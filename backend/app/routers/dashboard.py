from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.database import get_db
from app.models import Project, Character, Episode, Scene, GenerationTask
from app.config import settings

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/stats")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    total_projects = await db.scalar(select(func.count(Project.id))) or 0
    total_characters = await db.scalar(select(func.count(Character.id))) or 0
    total_episodes = await db.scalar(select(func.count(Episode.id))) or 0
    
    total_scenes = await db.scalar(select(func.count(Scene.id))) or 0
    total_images = await db.scalar(select(func.count(Scene.id)).where(Scene.image_path.isnot(None))) or 0
    total_videos = await db.scalar(select(func.count(Scene.id)).where(Scene.video_path.isnot(None))) or 0

    # Recent projects
    res_proj = await db.execute(select(Project).order_by(Project.created_at.desc()).limit(5))
    recent_projects = res_proj.scalars().all()

    # Recent tasks
    res_tasks = await db.execute(select(GenerationTask).order_by(GenerationTask.created_at.desc()).limit(10))
    recent_tasks = res_tasks.scalars().all()

    # System Status & Provider Config
    api_status = {
        "gemini": bool(settings.GEMINI_API_KEY),
        "elevenlabs": bool(settings.ELEVENLABS_API_KEY),
        "kling": bool(settings.KLING_API_KEY),
        "replicate": bool(settings.REPLICATE_API_TOKEN),
        "ffmpeg": True,
        "edge_tts": True,
        "pollinations": True
    }

    return {
        "counts": {
            "projects": total_projects,
            "characters": total_characters,
            "episodes": total_episodes,
            "scenes": total_scenes,
            "images": total_images,
            "videos": total_videos
        },
        "api_status": api_status,
        "recent_projects": [
            {
                "id": p.id,
                "name": p.name,
                "genre": p.genre,
                "language": p.language,
                "created_at": p.created_at.isoformat() if p.created_at else None
            } for p in recent_projects
        ],
        "recent_tasks": [
            {
                "id": t.id,
                "task_type": t.task_type,
                "status": t.status,
                "progress": t.progress,
                "provider": t.provider,
                "cost_estimate": t.cost_estimate,
                "created_at": t.created_at.isoformat() if t.created_at else None
            } for t in recent_tasks
        ]
    }
