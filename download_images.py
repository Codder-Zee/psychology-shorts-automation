import requests, os

keywords = open("output/keywords.txt").read().splitlines()
os.makedirs("output/images", exist_ok=True)

for i, k in enumerate(keywords, start=1):
    url = f"https://source.unsplash.com/1080x1920/?{k.replace(' ', '%20')}"
    img = requests.get(url).content
    with open(f"output/images/scene_{i}.jpg", "wb") as f:
        f.write(img)

print("Images downloaded:", len(keywords))
