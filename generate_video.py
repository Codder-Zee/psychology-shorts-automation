from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip
)

# Load audio
audio = AudioFileClip("voice.mp3")
duration = audio.duration

# Background image (royalty-free)
bg = ImageClip("https://picsum.photos/1080/1920").set_duration(duration)

# Load subtitles safely
subs = []
try:
    subs = open("subs.txt", encoding="utf-8").read().splitlines()
except:
    subs = []

# Fallback if subtitles empty
if not subs:
    subs = ["Psychology ke mutabik dimag aadaton se control hota hai"]

clips = []
start = 0
gap = duration / len(subs)

for line in subs:
    txt = TextClip(
        line,
        fontsize=60,
        font="DejaVu-Sans",          # ✅ safer font for GitHub runner
        color="white",
        stroke_color="black",
        stroke_width=2,
        size=(900, None),
        method="caption"
    ).set_position(("center", "bottom")) \
     .set_start(start) \
     .set_duration(gap)

    clips.append(txt)
    start += gap

# Final video
video = CompositeVideoClip([bg, *clips]).set_audio(audio)

video.write_videofile(
    "short.mp4",
    fps=24,
    codec="libx264",
    audio_codec="aac",
    verbose=False,
    logger=None
)
