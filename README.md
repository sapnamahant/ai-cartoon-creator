# AI Cartoon Studio – Automated 3D Animation Creator

A full-stack, modular AI-powered studio application for generating 3D animated cartoon episodes from story prompt to final assembled MP4.

## System Architecture

- **Frontend**: React + Vite + Tailwind CSS + Lucide Icons (`http://127.0.0.1:5173`)
- **Backend**: Python FastAPI with asynchronous task orchestration (`http://127.0.0.1:8000`)
- **Database**: SQLite with SQLAlchemy ORM (PostgreSQL ready)
- **AI Story Engine**: Google Gemini API (`gemini-2.5-flash`) + procedural fallback
- **Visuals & 3D Styling**: Modular image provider (Pollinations / Replicate / Local artistic slate engine)
- **Voice Studio**: Edge-TTS (multilingual neural voices: Hindi & Indian English) + ElevenLabs
- **Video Assembly**: FFmpeg v7.1 engine (`imageio-ffmpeg`) for Ken Burns camera motion, audio mix, and MP4 concatenation.

---

## Getting Started

### 1. Backend

```bash
cd backend
python -m pip install -r requirements.txt
python run.py
```
Backend will start on `http://127.0.0.1:8000`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```
Frontend will start on `http://127.0.0.1:5173`.

---

## Seeded Demo Project

**Series**: *THE VILLAGE OF SHADOWS – परछाइयों का गाँव*
- **Episode 1**: *The Village That Disappears*
- **Characters**: Aanya, Kabir, Meera, Arjun (with consistent wardrobe locks and voice profiles).
