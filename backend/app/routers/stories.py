from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from typing import Optional, List
from app.database import get_db
from app.models import Project, Episode, Scene, Dialogue, Character
from app.services.gemini_story import StoryGeneratorService

router = APIRouter(prefix="/api/stories", tags=["Stories"])

class StoryGenRequest(BaseModel):
    project_id: int
    idea: str
    genre: Optional[str] = "Horror + Mystery + Comedy"
    language: Optional[str] = "Hinglish"
    duration: Optional[str] = "2-5 minutes"

@router.post("/generate")
async def generate_story_and_episode(data: StoryGenRequest, db: AsyncSession = Depends(get_db)):
    # Fetch project & characters
    stmt = select(Project).where(Project.id == data.project_id).options(selectinload(Project.characters))
    res = await db.execute(stmt)
    proj = res.scalars().first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")

    chars = [
        {
            "id": c.id,
            "name": c.name,
            "age": c.age,
            "personality": c.personality,
            "appearance": c.appearance,
            "clothing": c.clothing
        } for c in proj.characters
    ]

    # Call Story AI Service
    script_data = await StoryGeneratorService.generate_script(
        idea=data.idea,
        genre=data.genre or proj.genre,
        language=data.language or proj.language,
        duration=data.duration or proj.target_duration,
        characters=chars
    )

    # Save as new Episode
    episode = Episode(
        project_id=proj.id,
        title=script_data.get("title", "New AI Generated Episode"),
        synopsis=script_data.get("synopsis", data.idea),
        status="scripted"
    )
    db.add(episode)
    await db.flush()

    char_name_to_id = {c.name.lower(): c.id for c in proj.characters}

    for sc in script_data.get("scenes", []):
        scene = Scene(
            episode_id=episode.id,
            scene_number=sc.get("scene_number", 1),
            title=sc.get("title", f"Scene {sc.get('scene_number', 1)}"),
            description=sc.get("description", ""),
            visual_prompt=sc.get("visual_prompt", ""),
            animation_prompt=sc.get("animation_prompt", "Cinematic camera movement"),
            duration_seconds=sc.get("duration_seconds", 4.0)
        )
        db.add(scene)
        await db.flush()

        for idx, d in enumerate(sc.get("dialogues", [])):
            speaker = d.get("speaker_name", "")
            cid = char_name_to_id.get(speaker.lower())
            diag = Dialogue(
                scene_id=scene.id,
                character_id=cid,
                speaker_name=speaker,
                text=d.get("text", ""),
                order=idx + 1
            )
            db.add(diag)

    await db.commit()
    await db.refresh(episode)

    return {
        "status": "success",
        "episode_id": episode.id,
        "title": episode.title,
        "scenes_count": len(script_data.get("scenes", []))
    }
