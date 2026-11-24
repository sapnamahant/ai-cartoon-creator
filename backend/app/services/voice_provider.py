import os
import subprocess
import asyncio
import urllib.parse
import imageio_ffmpeg
import httpx
from app.config import settings

AVAILABLE_VOICES = [
    {
        "id": "hi-male-deep",
        "name": "Arjun (Hindi/Hinglish - Deep Male)",
        "gender": "Male",
        "lang": "Hindi / Hinglish",
        "g_lang": "hi",
        "pitch_ratio": 0.80,
        "bass_boost": 6,
        "tempo": 0.95
    },
    {
        "id": "hi-male-youth",
        "name": "Kabir (Hindi/Hinglish - Expressive/Funny Male)",
        "gender": "Male",
        "lang": "Hindi / Hinglish",
        "g_lang": "hi",
        "pitch_ratio": 0.88,
        "bass_boost": 3,
        "tempo": 1.05
    },
    {
        "id": "hi-female-hero",
        "name": "Aanya (Hindi/Hinglish - Energetic Female)",
        "gender": "Female",
        "lang": "Hindi / Hinglish",
        "g_lang": "hi",
        "pitch_ratio": 1.12,
        "treble_boost": 4,
        "tempo": 1.02
    },
    {
        "id": "hi-female-smart",
        "name": "Meera (Hindi/Hinglish - Calm/Intellectual Female)",
        "gender": "Female",
        "lang": "Hindi / Hinglish",
        "g_lang": "hi",
        "pitch_ratio": 1.05,
        "treble_boost": 2,
        "tempo": 0.98
    },
    {
        "id": "en-male-narrator",
        "name": "Narrator (English - Deep Resonance)",
        "gender": "Male",
        "lang": "English",
        "g_lang": "en",
        "pitch_ratio": 0.82,
        "bass_boost": 7,
        "tempo": 0.95
    },
    {
        "id": "en-female-clear",
        "name": "Narrator / Host (English - Clear Female)",
        "gender": "Female",
        "lang": "English",
        "g_lang": "en",
        "pitch_ratio": 1.10,
        "treble_boost": 3,
        "tempo": 1.0
    }
]

class VoiceProvider:
    """Realistic & Gender-Accurate Voice Synthesis Engine."""

    @staticmethod
    def get_voice_profile(voice_id: str, character_name: str = ""):
        # Match by ID
        for v in AVAILABLE_VOICES:
            if v["id"] == voice_id:
                return v

        # Match by character name
        name_lower = character_name.lower()
        if "arjun" in name_lower:
            return AVAILABLE_VOICES[0]  # Deep Male
        elif "kabir" in name_lower:
            return AVAILABLE_VOICES[1]  # Expressive Male
        elif "aanya" in name_lower:
            return AVAILABLE_VOICES[2]  # Energetic Female
        elif "meera" in name_lower:
            return AVAILABLE_VOICES[3]  # Calm Female
        
        # Default fallback by gender heuristic in voice_id
        if "male" in voice_id.lower() or "madhur" in voice_id.lower() or "prabhat" in voice_id.lower() or "guy" in voice_id.lower():
            return AVAILABLE_VOICES[1]
        return AVAILABLE_VOICES[2]

    @staticmethod
    async def generate_speech(text: str, voice_id: str, filename: str, character_name: str = "", speed_rate: float = 1.0) -> str:
        out_dir = os.path.join(settings.MEDIA_DIR, "audio")
        os.makedirs(out_dir, exist_ok=True)
        final_file_path = os.path.join(out_dir, filename)
        raw_file_path = os.path.join(out_dir, f"raw_{filename}")

        # 1. ElevenLabs API if key configured
        if settings.ELEVENLABS_API_KEY:
            try:
                success = await VoiceProvider._generate_elevenlabs(text, voice_id, final_file_path)
                if success and os.path.exists(final_file_path) and os.path.getsize(final_file_path) > 1000:
                    return f"/media/audio/{filename}"
            except Exception as e:
                print(f"[VoiceProvider] ElevenLabs failed: {e}")

        # 2. Free High-Fidelity Neural Speech Generation + Gender Acoustic Post-Processing
        profile = VoiceProvider.get_voice_profile(voice_id, character_name)
        target_lang = profile.get("g_lang", "hi")

        try:
            encoded_text = urllib.parse.quote(text)
            tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_text}&tl={target_lang}&client=tw-ob"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
                resp = await client.get(tts_url, headers=headers)
                if resp.status_code == 200 and len(resp.content) > 1000:
                    with open(raw_file_path, "wb") as f:
                        f.write(resp.content)

                    # Gender-Acoustic Mastering via FFmpeg
                    await VoiceProvider._apply_gender_mastering(raw_file_path, final_file_path, profile, speed_rate)
                    
                    if os.path.exists(raw_file_path):
                        try:
                            os.remove(raw_file_path)
                        except Exception:
                            pass

                    print(f"[VoiceProvider] Successfully synthesized gender-mastered speech: {profile['name']} -> {filename}")
                    return f"/media/audio/{filename}"
        except Exception as e:
            print(f"[VoiceProvider] Spoken speech generation error: {e}")

        # 3. Clean synthetic audio generator fallback
        await VoiceProvider._generate_synthesized_tone(text, final_file_path, profile)
        return f"/media/audio/{filename}"

    @staticmethod
    async def _apply_gender_mastering(in_path: str, out_path: str, profile: dict, user_speed: float = 1.0):
        """Uses FFmpeg filtergraph to transform pitch, formants, resonance, and pacing to match authentic Male/Female acoustics."""
        ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
        pitch_ratio = profile.get("pitch_ratio", 1.0)
        tempo = profile.get("tempo", 1.0) * user_speed

        sample_rate = 24000
        shifted_rate = int(sample_rate * pitch_ratio)

        # Filters for rich acoustic warmth and natural timber
        filters = [
            f"asetrate={shifted_rate}",
            f"aresample={sample_rate}"
        ]

        if profile.get("gender") == "Male":
            bass = profile.get("bass_boost", 5)
            # Add chest resonance & chest cavity warmth
            filters.append(f"bass=g={bass}:f=140")
            filters.append("equalizer=f=120:t=q:w=1:g=3")
            filters.append("equalizer=f=3200:t=q:w=1.2:g=-2")
        else:
            treble = profile.get("treble_boost", 3)
            # Add crispness & vocal brightness
            filters.append(f"treble=g={treble}:f=3500")
            filters.append("equalizer=f=2800:t=q:w=1:g=2.5")
            filters.append("equalizer=f=180:t=q:w=1.5:g=-1.5")

        if tempo != 1.0:
            filters.append(f"atempo={tempo}")

        # Dynamic volume leveling & soft mastering limiter
        filters.append("loudnorm=I=-16:TP=-1.5:LRA=11")

        filter_str = ",".join(filters)

        cmd = [
            ffmpeg_bin,
            "-y",
            "-i", in_path,
            "-af", filter_str,
            "-c:a", "libmp3lame",
            "-b:a", "128k",
            out_path
        ]

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE))

    @staticmethod
    async def _generate_synthesized_tone(text: str, file_path: str, profile: dict):
        ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
        duration = max(2.0, min(8.0, len(text.split()) * 0.45))
        freq = 150 if profile.get("gender") == "Male" else 300
        
        cmd = [
            ffmpeg_bin,
            "-y",
            "-f", "lavfi",
            "-i", f"sine=frequency={freq}:duration={duration}",
            "-af", f"afade=t=in:ss=0:d=0.2,afade=t=out:st={duration-0.2}:d=0.2,volume=0.3",
            "-c:a", "libmp3lame",
            file_path
        ]
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE))

    @staticmethod
    async def _generate_elevenlabs(text: str, voice_id: str, file_path: str) -> bool:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": settings.ELEVENLABS_API_KEY
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2"
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json=data, headers=headers)
            if resp.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(resp.content)
                return True
        return False
