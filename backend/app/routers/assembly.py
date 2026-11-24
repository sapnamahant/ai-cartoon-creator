import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models import Episode, Scene, AudioTrack, Dialogue
from app.services.ffmpeg_assembly import VideoAssemblyService

router = APIRouter(prefix="/api/assembly", tags=["Video Assembly"])

class ExportEpisodeRequest(BaseModel):
    episode_id: int

@router.post("/export")
async def export_episode(data: ExportEpisodeRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(Episode).where(Episode.id == data.episode_id).options(
        selectinload(Episode.scenes).selectinload(Scene.dialogues),
        selectinload(Episode.audio_tracks)
    )
    res = await db.execute(stmt)
    episode = res.scalars().first()
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    # Collect scene videos or generate them if missing
    scene_videos = []
    for sc in sorted(episode.scenes, key=lambda s: s.scene_number):
        if sc.video_path:
            scene_videos.append(sc.video_path)
        elif sc.image_path:
            # Auto render clip
            vname = f"auto_clip_{sc.id}_{uuid.uuid4().hex[:4]}.mp4"
            vpath = await VideoAssemblyService.create_motion_clip_from_image(sc.image_path, sc.duration_seconds, vname)
            sc.video_path = vpath
            scene_videos.append(vpath)

    if not scene_videos:
        raise HTTPException(status_code=400, detail="Cannot export: No scene images or clips are available yet.")

    export_name = f"episode_{episode.id}_final_{uuid.uuid4().hex[:6]}.mp4"
    final_path = await VideoAssemblyService.assemble_full_episode(
        scene_video_paths=scene_videos,
        audio_tracks=[],
        out_filename=export_name
    )

    episode.video_export_path = final_path
    episode.status = "completed"
    await db.commit()
    await db.refresh(episode)

    return {
        "status": "success",
        "export_url": final_path,
        "episode_id": episode.id
    }
