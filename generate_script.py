import os
import sys
import requests
import traceback

HF_TOKEN = os.getenv("HF_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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

# ---------------- HF GENERATION ----------------
def generate_from_hf():
    if not HF_TOKEN:
        raise RuntimeError("HF_TOKEN missing")

    url = "https://router.huggingface.co/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [
            {"role": "user", "content": PROMPT}
        ],
        "max_tokens": 400,
        "temperature": 0.8
    }

    r = requests.post(url, headers=headers, json=payload, timeout=60)

    if r.status_code != 200:
        raise RuntimeError(f"HF API {r.status_code}: {r.text}")

    data = r.json()

    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        raise RuntimeError(f"HF invalid response format: {data}")


# ---------------- GEMINI GENERATION ----------------
def generate_from_gemini():
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY missing")

    import google.generativeai as genai

    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(PROMPT)

    if not response or not response.text:
        raise RuntimeError("Gemini returned empty response")

    return response.text


# ---------------- MAIN ----------------
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
        print("✅ Gemini success")

    except Exception as gemini_error:
        print("\n❌ Gemini ALSO FAILED")
        print("Reason:", gemini_error)
        print("\n--- FULL TRACEBACK ---")
        traceback.print_exc()
        sys.exit(1)

# ---------------- VALIDATION ----------------
lines = [l.strip() for l in text.split("\n") if l.strip()]

if len(lines) < 8:
    raise RuntimeError(f"Script too short ({len(lines)} scenes). Aborting.")

with open("script.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines[:12]))

print(f"🎬 Script generated: {len(lines[:12])} scenes")
