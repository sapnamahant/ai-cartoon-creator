import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models import Scene, Episode, Project, Character
from app.services.image_provider import ImageProvider
from app.services.ffmpeg_assembly import VideoAssemblyService

router = APIRouter(prefix="/api/scenes", tags=["Scenes"])

class SceneImageGenRequest(BaseModel):
    scene_id: int
    custom_prompt: Optional[str] = None

class SceneVideoGenRequest(BaseModel):
    scene_id: int
    animation_prompt: Optional[str] = None

@router.get("/episode/{episode_id}")
async def get_episode_scenes(episode_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Scene).where(Scene.episode_id == episode_id).options(
        selectinload(Scene.dialogues)
    ).order_by(Scene.scene_number)
    res = await db.execute(stmt)
    scenes = res.scalars().all()
    return scenes

@router.post("/generate-image")
async def generate_scene_image(data: SceneImageGenRequest, db: AsyncSession = Depends(get_db)):
    scene = await db.get(Scene, data.scene_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")

    episode = await db.get(Episode, scene.episode_id)
    project = await db.get(Project, episode.project_id) if episode else None
    style = project.visual_style if project else "Cinematic 3D animation"

    prompt_to_use = data.custom_prompt or scene.visual_prompt
    filename = f"scene_{scene.id}_{uuid.uuid4().hex[:6]}.jpg"

    image_rel_path = await ImageProvider.generate_scene_image(prompt_to_use, filename, style_prefix=style)
    scene.image_path = image_rel_path
    scene.is_image_approved = True
    await db.commit()
    await db.refresh(scene)

    return {"status": "success", "image_path": image_rel_path}

@router.post("/generate-video")
async def generate_scene_video(data: SceneVideoGenRequest, db: AsyncSession = Depends(get_db)):
    scene = await db.get(Scene, data.scene_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")

    if not scene.image_path:
        raise HTTPException(status_code=400, detail="Cannot generate video: Please generate an image for this scene first.")

    filename = f"clip_{scene.id}_{uuid.uuid4().hex[:6]}.mp4"
    video_rel_path = await VideoAssemblyService.create_motion_clip_from_image(
        image_path=scene.image_path,
        duration=scene.duration_seconds,
        out_filename=filename
    )

    scene.video_path = video_rel_path
    scene.is_video_approved = True
    await db.commit()
    await db.refresh(scene)

    return {"status": "success", "video_path": video_rel_path}
