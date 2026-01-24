import os
import requests
import sys
import google.generativeai as genai

# API Tokens
HF_TOKEN = os.getenv("HF_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

PROMPT = (
    "Write a Hindi psychology short video script.\n"
    "Length: 40 to 60 seconds.\n"
    "Structure:\n"
    "- 8 to 12 short scenes\n"
    "- Each scene on a new line\n"
    "- No emojis, No hashtags, No repetition\n"
)

def call_gemini():
    """Gemini API call with fix for 404 error"""
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY is not set in GitHub Secrets.")
        return None
    try:
        print("Attempting Gemini API Fallback...")
        genai.configure(api_key=GEMINI_API_KEY)
        
        # 'latest' suffix lagana zaroori hai 404 se bachne ke liye
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Psychology content block na ho isliye safety_settings use ki hain
        response = model.generate_content(
            PROMPT,
            safety_settings={
                'HATE': 'BLOCK_NONE',
                'HARASSMENT': 'BLOCK_NONE',
                'SEXUAL' : 'BLOCK_NONE',
                'DANGEROUS' : 'BLOCK_NONE'
            }
        )
        return response.text.strip()
    except Exception as e:
        print(f"Gemini Error: {e}")
        return None

# --- Flow Logic ---
# Pehle Gemini hi try karte hain kyunki ye zyada reliable hai
text = call_gemini()

if not text:
    print("Gemini failed, check your API key.")
    sys.exit(1)

# Script cleanup
lines = [l.strip() for l in text.split("\n") if l.strip()]

with open("script.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines[:12]))

print(f"Script generated successfully with {len(lines[:12])} scenes.")
