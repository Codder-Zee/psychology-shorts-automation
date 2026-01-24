import requests, os
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
from script_reader import read_next_script

WIDTH, HEIGHT = 1080, 1920

def download_image(keyword, idx):
    url = f"https://source.unsplash.com/1080x1920/?{keyword}"
    img = requests.get(url).content
    path = f"img_{idx}.jpg"
    with open(path, "wb") as f:
        f.write(img)
    return path

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
