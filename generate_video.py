from moviepy.editor import *

audio = AudioFileClip("voice.mp3")
duration = audio.duration

# background image
bg = ImageClip("https://picsum.photos/1080/1920").set_duration(duration)

# subtitles
subs = open("subs.txt", encoding="utf-8").read().splitlines()

clips = []
start = 0
gap = duration / len(subs)

for line in subs:
    txt = TextClip(
        line,
        fontsize=70,
        font="DejaVu-Sans-Bold",
        color="white",
        stroke_color="black",
        stroke_width=3,
        size=(900, None),
        method="caption"
    ).set_position(("center", "bottom")) \
     .set_start(start) \
     .set_duration(gap)

    clips.append(txt)
    start += gap

video = CompositeVideoClip([bg, *clips]).set_audio(audio)

video.write_videofile(
    "short.mp4",
    fps=24,
    codec="libx264",
    audio_codec="aac"
)
