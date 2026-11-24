import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models import Dialogue, Character
from app.services.voice_provider import VoiceProvider, AVAILABLE_VOICES

router = APIRouter(prefix="/api/voice", tags=["Voice"])

class VoiceGenRequest(BaseModel):
    dialogue_id: int
    voice_id: Optional[str] = None
    speed: Optional[float] = 1.0

@router.get("/available-voices")
async def get_available_voices():
    return AVAILABLE_VOICES

@router.post("/generate")
async def generate_dialogue_speech(data: VoiceGenRequest, db: AsyncSession = Depends(get_db)):
    diag = await db.get(Dialogue, data.dialogue_id)
    if not diag:
        raise HTTPException(status_code=404, detail="Dialogue not found")

    character_name = diag.speaker_name or ""
    voice_to_use = data.voice_id
    if not voice_to_use and diag.character_id:
        char = await db.get(Character, diag.character_id)
        if char:
            voice_to_use = char.voice_id
            character_name = char.name

    if not voice_to_use:
        voice_to_use = "hi-female-hero" if character_name.lower() in ["aanya", "meera"] else "hi-male-youth"

    filename = f"voice_{diag.id}_{uuid.uuid4().hex[:6]}.mp3"
    audio_path = await VoiceProvider.generate_speech(
        text=diag.text,
        voice_id=voice_to_use,
        filename=filename,
        character_name=character_name,
        speed_rate=data.speed or 1.0
    )

    diag.audio_path = audio_path
    await db.commit()
    await db.refresh(diag)

    return {"status": "success", "audio_path": audio_path}
