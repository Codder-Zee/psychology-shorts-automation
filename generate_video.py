import requests, os
from moviepy.editor import *
from PIL import Image
from io import BytesIO
from script_reader import read_next_script

WIDTH, HEIGHT = 1080, 1920

def download_image(keyword, idx):
    url = f"https://source.unsplash.com/1080x1920/?{keyword}"
    response = requests.get(url, timeout=20)

    try:
        # verify that real image is received
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")

        path = f"img_{idx}.jpg"
        img.save(path, "JPEG")
        return path

    except Exception as e:
        raise Exception(f"Invalid image downloaded for keyword: {keyword}") from e


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
