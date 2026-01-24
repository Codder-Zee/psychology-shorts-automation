import os
import sys
import google.generativeai as genai

# GitHub Secrets se key uthana
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

PROMPT = (
    "Write a Hindi psychology short video script.\n"
    "8 to 12 short scenes, each on a new line. No emojis."
)

def call_gemini():
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY missing in GitHub Secrets")
        return None
    
    try:
        print("Attempting Gemini API...")
        genai.configure(api_key=GEMINI_API_KEY)
        
        # FIX: 'models/' prefix hatana zaroori hai naye version mein
        # Aur sirf 'gemini-1.5-flash' use karein bina '-latest' ke
        model = genai.GenerativeModel('gemini-1.5-flash')
        
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
        # Agar naya version fail ho toh purana format try karega
        print(f"Direct call failed, trying alternative name: {e}")
        try:
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            response = model.generate_content(PROMPT)
            return response.text.strip()
        except Exception as e2:
            print(f"All attempts failed: {e2}")
            return None

# Execution logic
text = call_gemini()

if text:
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Success: Script generated!")
else:
    print("Gemini failed. Please check if the API Key is correct.")
    sys.exit(1)
