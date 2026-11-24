import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models import Character, Project
from app.services.image_provider import ImageProvider

router = APIRouter(prefix="/api/characters", tags=["Characters"])

class CharacterCreate(BaseModel):
    project_id: int
    name: str
    age: Optional[int] = 20
    personality: Optional[str] = ""
    appearance: Optional[str] = ""
    clothing: Optional[str] = ""
    voice_id: Optional[str] = "hi-IN-SwaraNeural"
    voice_style: Optional[str] = "Natural expressive"

class CharacterGenerateRef(BaseModel):
    character_id: int

@router.post("")
async def create_character(data: CharacterCreate, db: AsyncSession = Depends(get_db)):
    char = Character(**data.dict())
    db.add(char)
    await db.commit()
    await db.refresh(char)
    return char

@router.post("/generate-ref")
async def generate_character_reference(data: CharacterGenerateRef, db: AsyncSession = Depends(get_db)):
    char = await db.get(Character, data.character_id)
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")

    project = await db.get(Project, char.project_id)
    style = project.visual_style if project else "Cinematic 3D animation"

    prompt = (
        f"Character concept model sheet render: {char.name}, {char.age} years old. "
        f"Features: {char.appearance}. Wearing: {char.clothing}. Personality aura: {char.personality}. "
        f"Centered pose, full body turn-around view, neutral lighting, 3D character design."
    )

    filename = f"char_{char.id}_{uuid.uuid4().hex[:6]}.jpg"
    image_rel_path = await ImageProvider.generate_scene_image(prompt, filename, style_prefix=style)

    char.reference_image = image_rel_path
    await db.commit()
    await db.refresh(char)

    return {"status": "success", "image_url": image_rel_path, "character_id": char.id}

@router.post("/{character_id}/approve")
async def approve_character(character_id: int, db: AsyncSession = Depends(get_db)):
    char = await db.get(Character, character_id)
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")
    char.is_approved = True
    await db.commit()
    return {"status": "success", "is_approved": True}
