from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import requests
import os

audio = AudioFileClip("voice.mp3")

scenes = open("subs.txt", encoding="utf-8").read().splitlines()
if len(scenes) == 0:
    raise RuntimeError("No scenes found")

scene_duration = audio.duration / len(scenes)
clips = []

for i in range(len(scenes)):
    img_url = f"https://picsum.photos/1080/1920?random={i}"
    img_data = requests.get(img_url).content

    img_path = f"scene_{i}.jpg"
    with open(img_path, "wb") as f:
        f.write(img_data)

    clip = ImageClip(img_path).set_duration(scene_duration)
    clips.append(clip)

video = concatenate_videoclips(clips).set_audio(audio)

video.write_videofile(
    "short.mp4",
    fps=24,
    codec="libx264",
    audio_codec="aac",
    verbose=False,
    logger=None
)
