from moviepy.editor import *
import requests
import os

# Load voice
audio = AudioFileClip("voice.mp3")
total_duration = audio.duration

# Load script
with open("script.txt", encoding="utf-8") as f:
    scenes = f.read().splitlines()

scene_duration = total_duration / len(scenes)

clips = []
current_time = 0

for i, scene in enumerate(scenes):
    # Unique image per scene
    img_url = f"https://picsum.photos/1080/1920?random={i+1}"
    img_path = f"img_{i}.jpg"

    img_data = requests.get(img_url).content
    with open(img_path, "wb") as img:
        img.write(img_data)

    bg = (
        ImageClip(img_path)
        .set_duration(scene_duration)
        .resize(height=1920)
        .set_position("center")
    )

    txt = (
        TextClip(
            scene,
            fontsize=65,
            font="DejaVu-Sans-Bold",
            color="white",
            stroke_color="black",
            stroke_width=3,
            size=(900, None),
            method="caption"
        )
        .set_duration(scene_duration)
        .set_position(("center", "bottom"))
    )

    clip = CompositeVideoClip([bg, txt]).set_start(current_time)
    clips.append(clip)
    current_time += scene_duration

final = CompositeVideoClip(clips).set_audio(audio)

final.write_videofile(
    "short.mp4",
    fps=24,
    codec="libx264",
    audio_codec="aac"
    )
