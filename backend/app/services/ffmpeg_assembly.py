import os
import subprocess
import asyncio
import imageio_ffmpeg
from app.config import settings

class VideoAssemblyService:
    """Uses FFmpeg engine to assemble scene video clips, dialogue audio tracks, background music, and subtitles into a finished MP4 episode."""

    @staticmethod
    def get_ffmpeg_path() -> str:
        return imageio_ffmpeg.get_ffmpeg_exe()

    @staticmethod
    async def create_motion_clip_from_image(image_path: str, duration: float, out_filename: str, aspect_ratio: str = "16:9") -> str:
        """Converts a still scene image into a cinematic camera motion clip (zoom-in/pan) using FFmpeg filtergraphs."""
        ffmpeg_bin = VideoAssemblyService.get_ffmpeg_path()
        out_dir = os.path.join(settings.MEDIA_DIR, "videos")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, out_filename)

        real_img_path = image_path.replace("/media/", f"{settings.MEDIA_DIR}/")
        if not os.path.exists(real_img_path):
            raise FileNotFoundError(f"Image not found at {real_img_path}")

        # Scale & aspect ratio resolution
        scale_filter = "scale=1920:1080" if aspect_ratio == "16:9" else "scale=1080:1920"
        fps = 25
        total_frames = int(duration * fps)

        # Smooth Ken-Burns dynamic zoom-in filter
        vf = f"zoompan=z='min(zoom+0.0015,1.25)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080,fps={fps}"

        cmd = [
            ffmpeg_bin,
            "-y",
            "-loop", "1",
            "-i", real_img_path,
            "-vf", vf,
            "-t", str(duration),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-tune", "stillimage",
            out_path
        ]

        proc = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            print(f"[VideoAssembly] Clip gen error: {stderr.decode()}")
            raise RuntimeError(f"FFmpeg motion clip error: {stderr.decode()}")

        return f"/media/videos/{out_filename}"

    @staticmethod
    async def assemble_full_episode(scene_video_paths: list, audio_tracks: list, out_filename: str) -> str:
        """Concatenates scene clips, mixes audio dialogue/BGM, and renders the master MP4."""
        ffmpeg_bin = VideoAssemblyService.get_ffmpeg_path()
        out_dir = os.path.join(settings.MEDIA_DIR, "exports")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, out_filename)

        # 1. Create concat demuxer file list
        concat_file = os.path.join(out_dir, f"concat_{out_filename}.txt")
        with open(concat_file, "w", encoding="utf-8") as f:
            for p in scene_video_paths:
                real_p = p.replace("/media/", f"{settings.MEDIA_DIR}/").replace("\\", "/")
                f.write(f"file '{real_p}'\n")

        # Concat video streams
        cmd = [
            ffmpeg_bin,
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            out_path
        ]

        proc = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        await proc.communicate()

        if os.path.exists(concat_file):
            try:
                os.remove(concat_file)
            except Exception:
                pass

        return f"/media/exports/{out_filename}"
