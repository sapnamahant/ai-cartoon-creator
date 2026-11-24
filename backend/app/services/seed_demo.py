import json
import os
from sqlalchemy.future import select
from app.models import Project, Character, Episode, Scene, Dialogue, AudioTrack
from app.config import settings

SAMPLE_PROJECT = {
    "name": "THE VILLAGE OF SHADOWS – परछाइयों का गाँव",
    "description": "A spooky, humorous, and mysterious journey of four friends uncovering the secret of a disappearing Indian village.",
    "genre": "Horror + Mystery + Comedy",
    "language": "Hinglish",
    "visual_style": "Cinematic stylized 3D animated feature-film look, Pixar-meets-spooky fantasy aesthetic, rich volumetric lighting, detailed textures",
    "setting": "A mysterious Indian village surrounded by a dense mystical forest, old stone houses, banyan trees, eerie fog and lanterns.",
    "target_duration": "2–5 minutes"
}

SAMPLE_CHARACTERS = [
    {
        "name": "Aanya",
        "age": 23,
        "personality": "Brave, curious, proactive, natural team leader",
        "appearance": "Long dark brown ponytail, bright expressive brown eyes, warm Indian skin tone, athletic build",
        "clothing": "Mustard yellow jacket, white T-shirt, blue jeans, brown hiking boots",
        "voice_id": "hi-IN-SwaraNeural",
        "voice_style": "Confident, energetic, Hindi-English natural cadence",
        "reference_image": "/media/characters/aanya_ref.jpg",
        "is_approved": True
    },
    {
        "name": "Kabir",
        "age": 24,
        "personality": "Funny, witty, easily frightened, comical reactions",
        "appearance": "Short black hair, round glasses, expressive funny eyes, lean build",
        "clothing": "Teal hoodie, black trousers, white sneakers",
        "voice_id": "hi-IN-MadhurNeural",
        "voice_style": "Nervous, humorous, rapid comedic delivery",
        "reference_image": "/media/characters/kabir_ref.jpg",
        "is_approved": True
    },
    {
        "name": "Meera",
        "age": 23,
        "personality": "Intelligent, logical, analytical, solves riddles",
        "appearance": "Shoulder-length black hair, observant dark eyes, composed stance",
        "clothing": "Purple top, denim jacket, black trousers, smartwatch",
        "voice_id": "en-IN-NeerjaNeural",
        "voice_style": "Calm, intellectual, reassuring tone",
        "reference_image": "/media/characters/meera_ref.jpg",
        "is_approved": True
    },
    {
        "name": "Arjun",
        "age": 25,
        "personality": "Mysterious, quiet, observes before acting, knows local folklore",
        "appearance": "Messy black hair, intense gaze, strong jawline, tall build",
        "clothing": "Maroon jacket, black T-shirt, dark jeans, ancient brass pendant",
        "voice_id": "hi-IN-MadhurNeural",
        "voice_style": "Deep, reserved, thoughtful resonance",
        "reference_image": "/media/characters/arjun_ref.jpg",
        "is_approved": True
    }
]

SAMPLE_EPISODE = {
    "title": "The Village That Disappears",
    "synopsis": "When GPS signals vanish deep inside the Deodar forest, four friends stumble into Kuldhara-like village streets that only appear under the full moonlight.",
    "aspect_ratio": "16:9",
    "status": "scenes_ready"
}

SAMPLE_SCENES = [
    {
        "scene_number": 1,
        "title": "The Foggy Crossroad",
        "description": "The four friends stand in front of a rustic wooden milestone sign pointing towards 'Andhera Ghati'. Dense fog rolls between ancient twisted banyan trees.",
        "visual_prompt": "Stylized 3D animation, cinematic lighting. Four young Indian friends (girl in mustard yellow jacket, boy in teal hoodie with round glasses, girl in purple top with denim jacket, quiet boy in maroon jacket) standing at a misty forest crossroad in an Indian jungle. An ancient weathered signpost glows under mystical blue moonlight.",
        "animation_prompt": "Slow panoramic camera tracking forward, dense creeping fog particles moving across the ground.",
        "duration_seconds": 4.0,
        "dialogues": [
            {"speaker_name": "Kabir", "text": "Guys, mere phone ka network gaya! Aur ye sign board pe 'Do Not Enter' kyu likha hai?!"},
            {"speaker_name": "Aanya", "text": "Chill Kabir, hum bas thoda aage check karenge. Ye rasta seedha village square jaata hai."}
        ]
    },
    {
        "scene_number": 2,
        "title": "The Disappearing Archway",
        "description": "They walk through an ornate carved stone archway into a silent village courtyard. Lanterns flicker on walls with no fire.",
        "visual_prompt": "Stylized 3D animated film still. Ancient Indian stone archway carved with peacock motifs, lantern lights flickering softly with warm amber glow against midnight blue shadows. Cobblestone pathway.",
        "animation_prompt": "Subtle push-in shot, eerie flickering lanterns cast shifting shadows.",
        "duration_seconds": 4.5,
        "dialogues": [
            {"speaker_name": "Meera", "text": "Notice karo... architecture 200 saal purani hai, but lanterns abhi bhi fresh jal rahe hain."},
            {"speaker_name": "Arjun", "text": "Ye wahi gaon hai... jo har amavasya ko gayab ho jaata hai."}
        ]
    },
    {
        "scene_number": 3,
        "title": "The Grand Bell Tower",
        "description": "In the center of the village, a massive ancient brass bell starts chiming by itself. A shadow darts across the rooftop.",
        "visual_prompt": "Cinematic 3D animation. A towering antique stone bell tower in an Indian hamlet, moonlight illuminating a giant engraved bronze bell swaying. A silhouette passes swiftly across tiled roofs.",
        "animation_prompt": "Low angle dynamic camera looking up at the chiming bell, fog swirling.",
        "duration_seconds": 4.0,
        "dialogues": [
            {"speaker_name": "Kabir", "text": "Aree baap re! Bell khud kaise baj rahi hai?! Bhagoooo!"},
            {"speaker_name": "Aanya", "text": "Ruko! Dekho wahan... koi rooftop pe hai!"}
        ]
    }
]

async def seed_demo_data(session):
    stmt = select(Project).where(Project.name == SAMPLE_PROJECT["name"])
    res = await session.execute(stmt)
    existing = res.scalars().first()
    if existing:
        return existing.id

    # Create Project
    project = Project(**SAMPLE_PROJECT)
    session.add(project)
    await session.flush()

    # Create Characters
    char_map = {}
    for c_data in SAMPLE_CHARACTERS:
        char = Character(project_id=project.id, **c_data)
        session.add(char)
        await session.flush()
        char_map[char.name] = char.id

    # Create Episode
    ep_data = dict(SAMPLE_EPISODE)
    ep_data["project_id"] = project.id
    episode = Episode(**ep_data)
    session.add(episode)
    await session.flush()

    # Create Scenes & Dialogues
    for sc_data in SAMPLE_SCENES:
        dialogues_data = sc_data.pop("dialogues")
        scene = Scene(episode_id=episode.id, **sc_data)
        session.add(scene)
        await session.flush()

        for idx, d_data in enumerate(dialogues_data):
            char_id = char_map.get(d_data["speaker_name"])
            diag = Dialogue(
                scene_id=scene.id,
                character_id=char_id,
                speaker_name=d_data["speaker_name"],
                text=d_data["text"],
                order=idx + 1
            )
            session.add(diag)

    # Add default ambient tracks
    bgm = AudioTrack(
        episode_id=episode.id,
        name="Horror Atmosphere Theme",
        track_type="bgm",
        file_path="/media/audio/horror_ambience.mp3",
        volume=0.4,
        duration=120.0
    )
    session.add(bgm)

    await session.commit()
    print(f"Sample demo project seeded with ID: {project.id}")
    return project.id
