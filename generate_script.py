import os
import requests
import sys
import google.generativeai as genai

HF_TOKEN = os.getenv("HF_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def call_gemini():
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY missing in GitHub Secrets")
        return None
    try:
        print("Attempting Gemini API Fallback...")
        genai.configure(api_key=GEMINI_API_KEY)
        # FIX: Added '-latest' to avoid 404 error
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = "Write 10 short Hindi psychology facts for YouTube shorts. One fact per line. No emojis."
        
        response = model.generate_content(
            prompt,
            safety_settings={'HATE': 'BLOCK_NONE', 'HARASSMENT': 'BLOCK_NONE', 'SEXUAL': 'BLOCK_NONE', 'DANGEROUS': 'BLOCK_NONE'}
        )
        return response.text.strip()
    except Exception as e:
        print(f"Gemini Error: {e}")
        return None

# Main Flow
text = call_gemini() # Seedha Gemini try kar rahe hain testing ke liye

if text:
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Script generated successfully!")
else:
    print("API Failed.")
    sys.exit(1)
  
