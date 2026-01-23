from moviepy.editor import *
import os
import sys

VOICE = "assets/voice.mp3"
IMG_DIR = "assets/images"
SCRIPT = "assets/script.txt"

# ---- HARD VALIDATION ----
if not os.path.exists(VOICE):
    print("❌ voice.mp3 missing. Generate audio locally first.")
    sys.exit(1)

if not os.path.exists(SCRIPT):
    print("❌ script.txt missing.")
    sys.exit(1)

if not os.path.exists(IMG_DIR):
    print("❌ images folder missing.")
    sys.exit(1)

with open(SCRIPT, encoding="utf-8") as f:
    scenes = [l.strip() for l in f if l.strip()]

if len(scenes) < 8:
    print("❌ Not enough scenes for 40–60 sec video.")
    sys.exit(1)

audio = AudioFileClip(VOICE)
scene_duration = audio.duration / len(scenes)

clips = []

for i in range(len(scenes)):
    img_path = f"{IMG_DIR}/scene_{i+1}.jpg"
    if not os.path.exists(img_path):
        print(f"❌ Missing image: {img_path}")
        sys.exit(1)

    clip = (
        ImageClip(img_path)
        .set_duration(scene_duration)
        .resize((1080, 1920))
    )
    clips.append(clip)

video = concatenate_videoclips(clips, method="compose")
video = video.set_audio(audio)

video.write_videofile(
    "final_short.mp4",
    fps=24,
    codec="libx264",
    audio_codec="aac",
)

print("✅ Video generated successfully")
