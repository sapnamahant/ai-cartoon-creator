# Project: AI Cartoon Studio – Automated 3D Animation Creator

Act as a senior full-stack developer, AI engineer, UI/UX designer, and automation architect.

I want to build a complete AI-powered Cartoon Animation Studio application. The application should help users create animated cartoon episodes using AI, starting from a story idea and ending with an exported animated video.

Do not build only a static dashboard or demo. Build a functional, modular application with a clean interface, backend, database, API integrations, and a scalable architecture.

## 1. Main Objective

Create an AI Cartoon Studio that automates these steps:

1. Generate stories and episode scripts using AI.
2. Create and manage consistent cartoon characters.
3. Generate scene backgrounds and character images.
4. Convert images into animated video clips.
5. Generate character voices and dialogue.
6. Add background music and sound effects.
7. Automatically combine scenes, voices, subtitles, and audio.
8. Export the completed cartoon episode as an MP4 video.

## 2. Technology Stack

Use the following technologies:

- Frontend: React with a modern responsive UI.
- Backend: Python with FastAPI.
- Database: SQLite initially, with PostgreSQL support for future scaling.
- AI story generation: Google Gemini API.
- Image generation: Create a provider integration layer supporting available image-generation APIs.
- Video generation: Create an integration layer for image-to-video APIs such as Kling AI, subject to API availability.
- Voice generation: ElevenLabs API integration.
- Video editing: FFmpeg.
- Background jobs: Celery or a suitable task queue.
- Configuration: Environment variables stored in a secure .env file.

Keep all API integrations modular so providers can be replaced without rewriting the application.

## 3. Application Modules

### Module A: Dashboard
Create a dashboard showing:
- Total projects
- Total episodes
- Total characters
- Generated images
- Generated video clips
- Recent projects
- Generation task status

### Module B: Story Generator
Allow users to:
- Enter a story idea.
- Select genre: Horror, Comedy, Mystery, Adventure, Fantasy, Educational.
- Select language: Hindi, English, Hinglish.
- Select target duration: 1–2, 2–5, or 5–10 minutes.
- Generate episode titles.
- Generate complete scripts.
- Divide scripts into scenes.
- Generate dialogues for each character.
- Generate visual prompts for every scene.
- Edit and save generated scripts.

### Module C: Character Studio
Allow users to:
- Create original cartoon characters.
- Enter character name, age, personality, appearance, clothing, and voice style.
- Generate character reference images.
- Save approved character designs.
- Maintain consistent character descriptions and reference images across episodes.
- Reuse characters in multiple scenes and episodes.

### Module D: Scene Generator
For every scene:
- Display scene number and description.
- Display characters appearing in the scene.
- Generate a visual prompt.
- Generate a background image.
- Generate character images.
- Allow users to regenerate or approve images.
- Maintain a consistent visual style and character appearance.

### Module E: Image-to-Video Generator
Allow users to:
- Select an approved scene image.
- Enter animation instructions.
- Generate a video clip using a connected video-generation provider.
- Set clip duration and aspect ratio.
- Preview generated clips.
- Regenerate or approve clips.
- Track generation status and errors.

### Module F: Voice Studio
Allow users to:
- Generate dialogue audio for each character.
- Select different voices for different characters.
- Configure language, voice style, and speaking speed.
- Generate narration.
- Preview audio.
- Save audio files and associate them with scenes.

### Module G: Audio and Sound Effects
Add:
- Background music.
- Horror atmosphere.
- Footsteps.
- Door sounds.
- Wind and forest sounds.
- Bell sounds.
- Character-specific sound effects.

Allow users to upload their own audio files as well.

### Module H: Video Editor
Build an automatic video assembly system using FFmpeg.

It should:
- Combine scene clips in the correct order.
- Add character dialogue.
- Add narration.
- Add background music and sound effects.
- Add subtitles.
- Support transitions.
- Allow basic scene ordering and trimming.
- Export final videos in MP4 format.
- Support 16:9 and 9:16 aspect ratios.

### Module I: Project and Episode Management
Allow users to:
- Create multiple cartoon series.
- Create multiple seasons.
- Create multiple episodes.
- Save characters and scripts.
- Reuse characters and backgrounds.
- Save generation history.
- Download completed episodes.

## 4. First Demo Project

Create the following project as sample data:

Series Name: THE VILLAGE OF SHADOWS – परछाइयों का गाँव

Genre: Horror + Mystery + Comedy

Language: Hinglish

Visual Style: Cinematic stylized 3D animated feature-film look.

Setting: A mysterious Indian village surrounded by a dense forest.

Episode Duration: 2–5 minutes.

Audience: All age groups.

Characters:

1. Aanya – 23 years old, brave and curious, long dark brown ponytail, mustard yellow jacket, white T-shirt, blue jeans.
2. Kabir – 24 years old, funny and easily frightened, short black hair, round glasses, teal hoodie, black trousers.
3. Meera – 23 years old, intelligent and logical, shoulder-length black hair, purple top, denim jacket, black trousers.
4. Arjun – 25 years old, mysterious and quiet, messy black hair, maroon jacket, black T-shirt, dark jeans.

Important: Maintain consistent character appearance across every generated scene. Do not randomly change hairstyles, clothing, facial features, or body proportions.

Create the first episode as sample content:
"The Village That Disappears"

Use a spooky but family-friendly atmosphere, mystery, suspense, and comedy.

## 5. UI/UX Requirements

Design a professional, modern AI studio interface.

Use:
- Sidebar navigation.
- Dashboard cards.
- Project thumbnails.
- Character preview cards.
- Scene timeline.
- Image and video previews.
- Generation progress indicators.
- Clear buttons for Generate, Regenerate, Approve, Preview, and Export.

The interface must be responsive and easy for beginners to use.

## 6. Important Development Requirements

- Build the application in small, testable modules.
- Create a clear project folder structure.
- Use reusable components.
- Implement proper validation and error handling.
- Never expose API keys in frontend code.
- Store API keys securely in environment variables.
- Add API connection status indicators.
- Add retry functionality for failed generation tasks.
- Track generation costs where provider pricing information is available.
- Do not hardcode fake successful API responses.
- If an API key is missing, show a clear setup message.
- Use mock mode only for development and label mock results clearly.
- Save generated assets and associate them with their projects and scenes.
- Provide setup instructions and documentation.

## 7. Development Workflow

Before writing code:

1. Analyze the complete project requirements.
2. Prepare the application architecture.
3. Create the database schema.
4. Prepare the folder structure.
5. Identify the required external APIs and their current integration requirements.
6. Explain which integrations require API keys or paid subscriptions.

Then implement the application step by step.

Start with:
Phase 1: Project setup, database, authentication, dashboard, and project management.

Phase 2: Story Generator and Character Studio.

Phase 3: Scene Generator and image generation.

Phase 4: Video generation and Voice Studio.

Phase 5: FFmpeg video assembly and export.

Phase 6: Testing, error handling, documentation, and deployment.

After completing each phase:
- Run the application.
- Test the implemented features.
- Fix errors.
- Explain what was completed.
- Tell me the next steps.

Do not attempt to implement every module in one untested code-generation step. Prioritize a working foundation and integrate real APIs incrementally.

My goal is to have a working AI Cartoon Studio that can eventually generate complete animated cartoon episodes with minimal manual effort.