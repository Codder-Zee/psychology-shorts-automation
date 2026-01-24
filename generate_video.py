from moviepy.editor import *
import requests
import os

# Voice aur Script load karein
if not os.path.exists("voice.mp3") or not os.path.exists("script.txt"):
    print("Error: Voice ya Script missing hai!")
    exit(1)

audio = AudioFileClip("voice.mp3")
total_duration = audio.duration

with open("script.txt", encoding="utf-8") as f:
    scenes = [l.strip() for l in f.readlines() if l.strip()]

scene_duration = total_duration / len(scenes)
clips = []
current_time = 0

print(f"Video generate ho raha hai... Scenes: {len(scenes)}")

for i, scene in enumerate(scenes):
    img_path = f"img_{i}.jpg"
    img_url = f"https://picsum.photos/1080/1920?random={i+10}" # Randomness badha di

    # Image download logic
    try:
        img_data = requests.get(img_url, timeout=20).content
        with open(img_path, "wb") as img:
            img.write(img_data)
    except:
        print(f"Image {i} download fail hui!")
        continue

    bg = (
        ImageClip(img_path)
        .set_duration(scene_duration)
        .resize(height=1920)
        .set_position("center")
    )

    txt = (
        TextClip(
            scene,
            fontsize=60,
            font="DejaVu-Sans-Bold",
            color="white",
            stroke_color="black",
            stroke_width=2,
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
final.write_videofile("short.mp4", fps=24, codec="libx264", audio_codec="aac")
  
