import requests, os
from io import BytesIO

# 🔥 FIX FOR PIL ANTIALIAS REMOVAL
from PIL import Image
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

from moviepy.editor import *
from script_reader import read_next_script

WIDTH, HEIGHT = 1080, 1920


def download_image(keyword, idx):
    urls = [
        f"https://source.unsplash.com/1080x1920/?{keyword}",
        "https://picsum.photos/1080/1920"
    ]

    for url in urls:
        try:
            response = requests.get(url, timeout=20)
            img = Image.open(BytesIO(response.content)).convert("RGB")

            path = f"img_{idx}.jpg"
            img.save(path, "JPEG")
            return path

        except Exception:
            continue

    raise Exception(f"All image sources failed for keyword: {keyword}")


def create_video():
    title, script, keywords = read_next_script()

    audio = AudioFileClip("voice.mp3")
    duration = audio.duration
    scene_duration = duration / len(keywords)

    clips = []
    for i, kw in enumerate(keywords):
        img_path = download_image(kw, i)

        clip = (
            ImageClip(img_path)
            .set_duration(scene_duration)
            .resize((WIDTH, HEIGHT))
            .crossfadein(0.4)
            .crossfadeout(0.4)
        )
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")
    video = video.set_audio(audio)
    video.write_videofile("final.mp4", fps=30)

    return title, script


if __name__ == "__main__":
    create_video()
