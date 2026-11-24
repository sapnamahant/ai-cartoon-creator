from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from typing import Optional, List
from app.database import get_db
from app.models import Project, Episode, Character

router = APIRouter(prefix="/api/projects", tags=["Projects"])

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    genre: Optional[str] = "Horror + Mystery + Comedy"
    language: Optional[str] = "Hinglish"
    visual_style: Optional[str] = "Cinematic stylized 3D animated feature-film look"
    setting: Optional[str] = ""
    target_duration: Optional[str] = "2-5 minutes"

@router.get("")
async def list_projects(db: AsyncSession = Depends(get_db)):
    stmt = select(Project).options(selectinload(Project.characters), selectinload(Project.episodes)).order_by(Project.created_at.desc())
    res = await db.execute(stmt)
    projects = res.scalars().all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "genre": p.genre,
            "language": p.language,
            "visual_style": p.visual_style,
            "setting": p.setting,
            "target_duration": p.target_duration,
            "character_count": len(p.characters),
            "episode_count": len(p.episodes),
            "created_at": p.created_at.isoformat() if p.created_at else None
        } for p in projects
    ]

@router.get("/{project_id}")
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Project).where(Project.id == project_id).options(
        selectinload(Project.characters),
        selectinload(Project.episodes).selectinload(Episode.scenes)
    )
    res = await db.execute(stmt)
    project = res.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "genre": project.genre,
        "language": project.language,
        "visual_style": project.visual_style,
        "setting": project.setting,
        "target_duration": project.target_duration,
        "characters": [
            {
                "id": c.id,
                "name": c.name,
                "age": c.age,
                "personality": c.personality,
                "appearance": c.appearance,
                "clothing": c.clothing,
                "voice_id": c.voice_id,
                "voice_style": c.voice_style,
                "reference_image": c.reference_image,
                "is_approved": c.is_approved
            } for c in project.characters
        ],
        "episodes": [
            {
                "id": ep.id,
                "title": ep.title,
                "synopsis": ep.synopsis,
                "status": ep.status,
                "scene_count": len(ep.scenes),
                "aspect_ratio": ep.aspect_ratio,
                "video_export_path": ep.video_export_path
            } for ep in project.episodes
        ]
    }

@router.post("")
async def create_project(data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    proj = Project(**data.dict())
    db.add(proj)
    await db.commit()
    await db.refresh(proj)
    return {"id": proj.id, "name": proj.name}
