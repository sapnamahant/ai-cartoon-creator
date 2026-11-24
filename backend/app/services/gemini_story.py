import os
import json
import re
from google import genai
from app.config import settings

class StoryGeneratorService:
    """Generates complete cartoon episode scripts, character breakdowns, and visual prompts using Google Gemini or intelligent fallback."""

    @staticmethod
    async def generate_script(idea: str, genre: str, language: str, duration: str, characters: list) -> dict:
        char_desc = "\n".join([f"- {c['name']} ({c.get('age', 20)}yo, {c.get('personality', '')}): wears {c.get('clothing', '')}" for c in characters])

        system_instruction = f"""
You are the Lead Writer and Director for a 3D Animated Cartoon Series.
Create an exciting, episodic cartoon script based on the user's premise.
Output STRICTLY valid JSON with no markdown wrapping or extra comments.

JSON Schema:
{{
  "title": "Episode Title",
  "synopsis": "Brief overview of the episode",
  "scenes": [
    {{
      "scene_number": 1,
      "title": "Scene Name",
      "description": "What happens in the scene",
      "visual_prompt": "Ultra-detailed visual prompt for 3D stylized animation. Include character appearance, clothing, environment, lighting, camera angle.",
      "animation_prompt": "Camera motion and character action instructions for image-to-video generation.",
      "duration_seconds": 4.5,
      "dialogues": [
        {{
          "speaker_name": "Character Name",
          "text": "Character dialogue in specified language"
        }}
      ]
    }}
  ]
}}
"""

        user_prompt = f"""
Story Idea: {idea}
Genre: {genre}
Language: {language}
Target Duration: {duration}
Consistent Characters:
{char_desc}

Generate a 3 to 5 scene script with vivid visual prompts, funny/dramatic dialogues, and clear continuity.
"""

        # If Gemini API Key is provided, call Google GenAI SDK
        if settings.GEMINI_API_KEY:
            try:
                client = genai.Client(api_key=settings.GEMINI_API_KEY)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"{system_instruction}\n\n{user_prompt}",
                    config={"response_mime_type": "application/json"}
                )
                if response.text:
                    parsed = json.loads(response.text)
                    return parsed
            except Exception as e:
                print(f"[StoryGenerator] Gemini API error: {e}. Using smart script generator.")

        # Fallback intelligent procedural script generator
        return StoryGeneratorService._generate_procedural_script(idea, genre, language, characters)

    @staticmethod
    def _generate_procedural_script(idea: str, genre: str, language: str, characters: list) -> dict:
        char_names = [c["name"] for c in characters] if characters else ["Aanya", "Kabir"]
        c1 = char_names[0]
        c2 = char_names[1] if len(char_names) > 1 else char_names[0]
        c3 = char_names[2] if len(char_names) > 2 else "Meera"

        return {
            "title": f"The Mystery of {idea.title()[:30]}",
            "synopsis": f"In this {genre.lower()} episode, our heroes confront a supernatural puzzle: {idea}.",
            "scenes": [
                {
                    "scene_number": 1,
                    "title": "The Awakening Riddle",
                    "description": f"{c1} and {c2} discover an anomaly connected to {idea}.",
                    "visual_prompt": f"Stylized 3D animated film render, Pixar-Disney aesthetic. {c1} and {c2} inspecting a glowing ancient artifact under moonlit mist in an Indian village. Cinematic depth of field, warm lantern bounce light.",
                    "animation_prompt": "Slow camera tracking shot circling around the characters, particle dust floating.",
                    "duration_seconds": 4.5,
                    "dialogues": [
                        {"speaker_name": c2, "text": f"Wait karo! Mujhe kuch ajeeb sa lag raha hai... ye normal nahi hai!" if "Hinglish" in language else "Wait! Something feels very strange here..."},
                        {"speaker_name": c1, "text": f"Daro mat {c2}, hume bas pata lagana hai ki sach kya hai." if "Hinglish" in language else f"Don't worry {c2}, we just need to uncover the truth."}
                    ]
                },
                {
                    "scene_number": 2,
                    "title": "The Hidden Chamber",
                    "description": f"{c3} deciphers the ancient inscriptions on the temple wall.",
                    "visual_prompt": f"Stylized 3D feature animation. {c3} standing inside a carved stone chamber with carved deities and ancient scripts glowing neon amber. Dramatic volumetric lighting.",
                    "animation_prompt": "Smooth push-in towards the glowing carvings, subtle eye movement from characters.",
                    "duration_seconds": 4.0,
                    "dialogues": [
                        {"speaker_name": c3, "text": "Symbols keh rahe hain ki agar humne bell bajayi, toh poora raasta khul jaayega!" if "Hinglish" in language else "The symbols indicate that the bell will open the path!"}
                    ]
                },
                {
                    "scene_number": 3,
                    "title": "The Grand Revelation",
                    "description": "The shadows swirl and a hidden passageway reveals the lost village secret.",
                    "visual_prompt": "Cinematic stylized 3D animation, climax scene. All friends standing together as a magical gateway of mist and fireflies reveals a hidden mystical kingdom.",
                    "animation_prompt": "Dramatic wide camera pull-out revealing the spectacular scale of the gateway.",
                    "duration_seconds": 5.0,
                    "dialogues": [
                        {"speaker_name": c1, "text": "Dekha?! Maine kaha tha na, parchaaiyon ke peeche sach hamesha chup nahi rehta!" if "Hinglish" in language else "See?! The truth cannot stay hidden behind the shadows forever!"},
                        {"speaker_name": c2, "text": "Haan lekin ab waapas jaane ka rasta kaun dhoondega?!" if "Hinglish" in language else "Great, but who will find the way back home?!"}
                    ]
                }
            ]
        }
