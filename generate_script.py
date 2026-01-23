import os
import sys
import traceback
import requests
import json

HF_TOKEN = os.getenv("HF_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

PROMPT = (
    "Write a Hindi psychology short video script.\n"
    "Length: 40 to 60 seconds.\n"
    "- 8 to 12 scenes\n"
    "- Each scene on new line\n"
    "- No emojis\n"
    "- No hashtags\n"
    "- No repetition\n"
)

def generate_from_hf():
    if not HF_TOKEN:
        raise RuntimeError("HF_TOKEN missing")

    url = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": PROMPT,
        "parameters": {
            "max_new_tokens": 450,
            "temperature": 0.8,
            "return_full_text": False
        }
    }

    res = requests.post(url, headers=headers, json=payload, timeout=60)

    if res.status_code != 200:
        raise RuntimeError(f"HF API {res.status_code}: {res.text}")

    data = res.json()
    if not isinstance(data, list) or "generated_text" not in data[0]:
        raise ValueError(f"HF invalid response: {data}")

    return data[0]["generated_text"]


def generate_from_gemini():
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY missing")

    from google.generativeai import configure, GenerativeModel
    configure(api_key=GEMINI_API_KEY)

    model = GenerativeModel("gemini-pro")
    response = model.generate_content(PROMPT)

    if not response or not response.text:
        raise RuntimeError("Gemini returned empty response")

    return response.text


try:
    print("▶ Trying HuggingFace...")
    text = generate_from_hf()
    print("✅ HuggingFace success")

except Exception as hf_error:
    print("\n⚠️ HuggingFace FAILED")
    print("Reason:", hf_error)
    print("↪ Switching to Gemini fallback\n")

    try:
        text = generate_from_gemini()
        print("✅ Gemini fallback success")

    except Exception as gemini_error:
        print("\n❌ Gemini ALSO FAILED")
        print("Reason:", gemini_error)
        print("\n--- FULL TRACEBACK ---")
        traceback.print_exc()
        sys.exit(1)

lines = [l.strip() for l in text.split("\n") if l.strip()]

if len(lines) < 8:
    raise RuntimeError(f"Script too short: {len(lines)} scenes")

with open("script.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines[:12]))

print(f"🎬 Script ready: {len(lines[:12])} scenes")
