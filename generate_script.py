import requests
import os
import sys

API_URL = "https://api-inference.huggingface.co/models/bigscience/bloomz"
headers = {
    "Authorization": f"Bearer {os.environ['HF_TOKEN']}"
}

prompt = (
    "Hindi me 6 scenes wali psychology short video script likho.\n"
    "Har scene 1–2 line ka ho.\n"
    "Topic: human behavior psychology.\n"
    "Tone: suspense + awareness.\n"
    "Total length 40–60 seconds.\n"
    "Har scene alag line me ho."
)

payload = {
    "inputs": prompt,
    "options": {"wait_for_model": True}
}

res = requests.post(API_URL, headers=headers, json=payload)

if res.status_code != 200:
    print("❌ Script generation failed")
    sys.exit(1)

data = res.json()

if not isinstance(data, list) or "generated_text" not in data[0]:
    print("❌ Invalid AI response")
    sys.exit(1)

text = data[0]["generated_text"].strip()

# Reject short / risky scripts
if len(text.split()) < 80:
    print("❌ Script too short")
    sys.exit(1)

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(text)
