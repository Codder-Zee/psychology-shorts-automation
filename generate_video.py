from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import requests
import textwrap

# Load audio
audio = AudioFileClip("voice.mp3")
duration = audio.duration

# Download background image
img_data = requests.get("https://picsum.photos/1080/1920").content
with open("bg.jpg", "wb") as f:
    f.write(img_data)

# Open image with PIL
img = Image.open("bg.jpg").convert("RGB")
draw = ImageDraw.Draw(img)

# Load subtitles
try:
    subs = open("subs.txt", encoding="utf-8").read().splitlines()
except:
    subs = []

if not subs:
    subs = ["Psychology ke mutabik insaan aadaton se control hota hai"]

# Font (Pillow default safe font)
font = ImageFont.load_default()

# Draw subtitles (center bottom)
y = 1500
for line in subs[:3]:
    wrapped = textwrap.fill(line, width=30)
    draw.text((100, y), wrapped, font=font, fill="white")
    y += 60

# Save final image
img.save("final_bg.jpg")

# Create video
bg_clip = ImageClip("final_bg.jpg").set_duration(duration)
video = bg_clip.set_audio(audio)

video.write_videofile(
    "short.mp4",
    fps=24,
    codec="libx264",
    audio_codec="aac",
    verbose=False,
    logger=None
)
