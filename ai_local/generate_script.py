import os
import sys
import requests
import json

HF_TOKEN = os.getenv("HF_TOKEN")

class ScriptGenerationError(Exception):
    pass

def generate_script():
    if not HF_TOKEN:
        raise ScriptGenerationError("HF_TOKEN missing")

    API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    prompt = (
        "Write a Hindi psychology short video script.\n"
        "Duration: 40–60 seconds.\n"
        "8 to 12 short scenes.\n"
        "Each scene on new line.\n"
        "No emojis. No hashtags. No repetition.\n"
        "Strong hook, emotional flow, practical insight."
    )

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.8,
            "return_full_text": False
        }
    }

    try:
        res = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    except Exception as e:
        raise ScriptGenerationError(f"Network error: {e}")

    if res.status_code != 200:
        raise ScriptGenerationError(f"HF API error {res.status_code}: {res.text}")

    try:
        data = res.json()
    except Exception:
        raise ScriptGenerationError("Invalid JSON response")

    if not isinstance(data, list) or "generated_text" not in data[0]:
        raise ScriptGenerationError(f"Unexpected response format: {data}")

    lines = [l.strip() for l in data[0]["generated_text"].split("\n") if l.strip()]

    if len(lines) < 8:
        raise ScriptGenerationError("Script too short (<8 scenes)")

    os.makedirs("../assets", exist_ok=True)
    with open("../assets/script.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines[:12]))

    print("✅ Script generated:", len(lines[:12]), "scenes")

if __name__ == "__main__":
    try:
        generate_script()
    except Exception as e:
        print("❌ SCRIPT ERROR:", e)
        sys.exit(1)
