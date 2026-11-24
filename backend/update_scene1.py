import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import AsyncSessionLocal
from app.models import Scene
from sqlalchemy import update

async def main():
    async with AsyncSessionLocal() as session:
        await session.execute(
            update(Scene)
            .where(Scene.id == 1)
            .values(
                image_path="/media/images/real_scene_1.jpg",
                video_path="/media/videos/real_scene_1_clip.mp4",
                is_image_approved=True,
                is_video_approved=True
            )
        )
        await session.commit()
        print("Updated Scene 1 with real 3D animation clip!")

if __name__ == "__main__":
    asyncio.run(main())
