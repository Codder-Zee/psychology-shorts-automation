from moviepy.editor import *
import os

audio = AudioFileClip("output/voice.mp3")
images = sorted(os.listdir("output/images"))

scene_duration = audio.duration / len(images)
clips = []

for img in images:
    clip = (
        ImageClip(f"output/images/{img}")
        .set_duration(scene_duration)
        .resize((1080,1920))
        .fadein(0.4)
        .fadeout(0.4)
    )
    clips.append(clip)

video = concatenate_videoclips(clips, method="compose").set_audio(audio)
video.write_videofile("output/final.mp4", fps=24, codec="libx264", audio_codec="aac")
