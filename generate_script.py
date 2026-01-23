import os
import requests
import sys
import json
import traceback

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN is missing in environment variables")

API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

PROMPT = (
    "Write a Hindi psychology short video script.\n"
    "Length: 40 to 60 seconds.\n"
    "Rules:\n"
    "- 8 to 12 scenes\n"
    "- Each scene on a new line\n"
    "- No emojis\n"
    "- No hashtags\n"
    "- No repetition\n"
)

payload = {
    "inputs": PROMPT,
    "parameters": {
        "max_new_tokens": 450,
        "temperature": 0.8,
        "return_full_text": False
    }
}

try:
    res = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)

    if res.status_code == 401:
        raise PermissionError("HF_TOKEN invalid or revoked")

    if res.status_code == 404:
        raise RuntimeError("Model not found on HuggingFace Router")

    if res.status_code == 429:
        raise RuntimeError("HuggingFace rate limit exceeded")

    if res.status_code != 200:
        raise RuntimeError(f"HF API error {res.status_code}: {res.text}")

    data = res.json()

    if not isinstance(data, list) or "generated_text" not in data[0]:
        raise ValueError(f"Unexpected HF response format: {json.dumps(data)[:200]}")

    text = data[0]["generated_text"].strip()
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    if len(lines) < 8:
        raise ValueError(f"Only {len(lines)} scenes generated — aborting")

    with open("script.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines[:12]))

    print(f"✅ Script generated successfully: {len(lines[:12])} scenes")

except Exception as e:
    print("\n❌ SCRIPT GENERATION FAILED")
    print("Reason:", str(e))
    print("\n--- TRACEBACK ---")
    traceback.print_exc()
    sys.exit(1)
