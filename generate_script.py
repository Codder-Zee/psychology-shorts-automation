import os
import requests
import sys

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    print("HF_TOKEN missing")
    sys.exit(1)

API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

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

# ✅ Router-compatible payload
payload = {
    "inputs": [
        {
            "role": "user",
            "content": PROMPT
        }
    ],
    "parameters": {
        "max_new_tokens": 600,
        "temperature": 0.8,
        "top_p": 0.9
    }
}

res = requests.post(API_URL, headers=headers, json=payload, timeout=90)

if res.status_code != 200:
    print("HF API failed:", res.text)
    sys.exit(1)

data = res.json()

# ✅ Router response handling
if isinstance(data, list) and "generated_text" in data[0]:
    text = data[0]["generated_text"]
elif isinstance(data, dict) and "choices" in data:
    text = data["choices"][0]["message"]["content"]
else:
    print("Invalid HF response:", data)
    sys.exit(1)

text = text.strip()
lines = [l.strip() for l in text.split("\n") if l.strip()]

# ❌ NO fallback — strict validation (as you asked)
if len(lines) < 8:
    print("Script too short, aborting")
    sys.exit(1)

with open("script.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines[:12]))

print("Script generated:", len(lines[:12]), "scenes")
