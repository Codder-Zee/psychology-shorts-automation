import os
import requests
import sys
import google.generativeai as genai

# API Tokens
HF_TOKEN = os.getenv("HF_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # GitHub Secrets mein add karein

API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"

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

def call_gemini():
    """Fallback function to generate script using Gemini"""
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY missing, cannot fallback.")
        return None
    
    try:
        print("Attempting Gemini API Fallback...")
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(PROMPT)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API also failed: {e}")
        return None

def call_huggingface():
    """Primary function to generate script using Hugging Face"""
    if not HF_TOKEN:
        print("HF_TOKEN missing")
        return None
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "inputs": [{"role": "user", "content": PROMPT}],
        "parameters": {"max_new_tokens": 600, "temperature": 0.8, "top_p": 0.9}
    }
    
    try:
        print("Attempting Hugging Face...")
        res = requests.post(API_URL, headers=headers, json=payload, timeout=90)
        if res.status_code != 200:
            return None
        
        data = res.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        elif isinstance(data, dict) and "choices" in data:
            return data["choices"][0]["message"]["content"]
        return None
    except Exception:
        return None

# --- Main Logic ---
text = call_huggingface()

if not text:
    text = call_gemini()

if not text:
    print("Both APIs failed. Aborting.")
    sys.exit(1)

text = text.strip()
lines = [l.strip() for l in text.split("\n") if l.strip()]

if len(lines) < 8:
    print("Script too short, aborting")
    sys.exit(1)

with open("script.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines[:12]))

print("Script generated successfully!")
