import os
import sys

class ImageGenerationError(Exception):
    pass

SCRIPT_PATH = "../assets/script.txt"
IMG_DIR = "../assets/images"

def generate_images():
    if not os.path.exists(SCRIPT_PATH):
        raise ImageGenerationError("script.txt missing")

    with open(SCRIPT_PATH, encoding="utf-8") as f:
        scenes = [l.strip() for l in f if l.strip()]

    os.makedirs(IMG_DIR, exist_ok=True)

    for i, scene in enumerate(scenes, start=1):
        img_path = f"{IMG_DIR}/scene_{i}.jpg"

        # placeholder (replace with SD / DALL·E / local AI later)
        with open(img_path, "wb") as f:
            f.write(b"")

    print("✅ Images prepared:", len(scenes))

if __name__ == "__main__":
    try:
        generate_images()
    except Exception as e:
        print("❌ IMAGE ERROR:", e)
        sys.exit(1)
