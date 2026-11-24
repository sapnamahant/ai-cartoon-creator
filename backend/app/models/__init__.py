import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    genre = Column(String(100), default="Horror + Mystery + Comedy")
    language = Column(String(50), default="Hinglish")
    visual_style = Column(String(255), default="Cinematic stylized 3D animated feature-film look")
    setting = Column(Text, default="A mysterious Indian village surrounded by a dense forest")
    target_duration = Column(String(50), default="2-5 minutes")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    characters = relationship("Character", back_populates="project", cascade="all, delete-orphan")
    episodes = relationship("Episode", back_populates="project", cascade="all, delete-orphan")

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, default=20)
    personality = Column(Text, default="")
    appearance = Column(Text, default="")
    clothing = Column(Text, default="")
    voice_id = Column(String(100), default="hi-IN-SwaraNeural")
    voice_style = Column(String(100), default="Expressive, natural")
    speed = Column(Float, default=1.0)
    reference_image = Column(String(500), nullable=True)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="characters")
    dialogues = relationship("Dialogue", back_populates="character")

class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    synopsis = Column(Text, nullable=True)
    status = Column(String(50), default="draft")  # draft, scripted, scenes_ready, rendering, completed
    aspect_ratio = Column(String(20), default="16:9") # 16:9, 9:16
    video_export_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="episodes")
    scenes = relationship("Scene", back_populates="episode", cascade="all, delete-orphan", order_by="Scene.scene_number")
    audio_tracks = relationship("AudioTrack", back_populates="episode", cascade="all, delete-orphan")

class Scene(Base):
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)
    episode_id = Column(Integer, ForeignKey("episodes.id"), nullable=False)
    scene_number = Column(Integer, nullable=False)
    title = Column(String(255), default="")
    description = Column(Text, nullable=False)
    visual_prompt = Column(Text, nullable=False)
    animation_prompt = Column(Text, default="Subtle camera push-in, cinematic natural character movement")
    duration_seconds = Column(Float, default=4.0)
    
    # Media paths
    image_path = Column(String(500), nullable=True)
    video_path = Column(String(500), nullable=True)
    is_image_approved = Column(Boolean, default=False)
    is_video_approved = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    episode = relationship("Episode", back_populates="scenes")
    dialogues = relationship("Dialogue", back_populates="scene", cascade="all, delete-orphan", order_by="Dialogue.order")
    sfx_tracks = relationship("AudioTrack", back_populates="scene")

class Dialogue(Base):
    __tablename__ = "dialogues"

    id = Column(Integer, primary_key=True, index=True)
    scene_id = Column(Integer, ForeignKey("scenes.id"), nullable=False)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=True)
    speaker_name = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    audio_path = Column(String(500), nullable=True)
    duration_seconds = Column(Float, default=2.5)
    order = Column(Integer, default=1)
    
    scene = relationship("Scene", back_populates="dialogues")
    character = relationship("Character", back_populates="dialogues")

class AudioTrack(Base):
    __tablename__ = "audio_tracks"

    id = Column(Integer, primary_key=True, index=True)
    episode_id = Column(Integer, ForeignKey("episodes.id"), nullable=False)
    scene_id = Column(Integer, ForeignKey("scenes.id"), nullable=True)
    name = Column(String(100), nullable=False)
    track_type = Column(String(50), default="bgm")  # bgm, sfx, ambience, voice
    file_path = Column(String(500), nullable=False)
    volume = Column(Float, default=0.5)
    start_time = Column(Float, default=0.0)
    duration = Column(Float, default=0.0)

    episode = relationship("Episode", back_populates="audio_tracks")
    scene = relationship("Scene", back_populates="sfx_tracks")

class GenerationTask(Base):
    __tablename__ = "generation_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String(50), nullable=False)  # story, image, video, voice, export
    entity_type = Column(String(50), nullable=True) # project, character, scene, episode
    entity_id = Column(Integer, nullable=True)
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    progress = Column(Integer, default=0)
    provider = Column(String(100), default="internal")
    cost_estimate = Column(Float, default=0.0)
    error_message = Column(Text, nullable=True)
    result_data = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
