from moviepy.editor import *
import os

IMG_DIR = "assets/images"
VOICE = "assets/voice.mp3"
SCRIPT = "assets/script.txt"

with open(SCRIPT, encoding="utf-8") as f:
    scenes = [l.strip() for l in f if l.strip()]

audio = AudioFileClip(VOICE)
scene_duration = audio.duration / len(scenes)

clips = []
for i in range(len(scenes)):
    img = ImageClip(f"{IMG_DIR}/scene_{i+1}.jpg") \
        .set_duration(scene_duration) \
        .resize((1080, 1920))
    clips.append(img)

video = concatenate_videoclips(clips).set_audio(audio)

video.write_videofile(
    "final_short.mp4",
    fps=24,
    codec="libx264",
    audio_codec="aac"
)

print("✅ Video generated")
