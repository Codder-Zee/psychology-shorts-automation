import os
import requests
import sys

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    print("HF_TOKEN missing")
    sys.exit(1)

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

PROMPT = (
    "Write a Hindi psychology short video script.\n"
    "Length: 40 to 60 seconds.\n"
    "Structure:\n"
    "- 8 to 12 short scenes\n"
    "- Each scene on a new line\n"
    "- No emojis\n"
    "- No hashtags\n"
    "- No repetition\n"
)

payload = {
    "inputs": PROMPT,
    "parameters": {
        "max_new_tokens": 350,
        "temperature": 0.8,
        "return_full_text": False
    }
}

res = requests.post(API_URL, headers=headers, json=payload, timeout=60)

if res.status_code != 200:
    print("HF API failed:", res.text)
    sys.exit(1)

data = res.json()

if not isinstance(data, list) or "generated_text" not in data[0]:
    print("Invalid HF response")
    sys.exit(1)

text = data[0]["generated_text"].strip()
lines = [l.strip() for l in text.split("\n") if l.strip()]

# ❌ NO fallback — strict validation
if len(lines) < 8:
    print("Script too short, aborting")
    sys.exit(1)

with open("script.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines[:12]))

print("Script generated:", len(lines[:12]), "scenes")
