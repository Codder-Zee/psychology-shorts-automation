import os
import sys
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

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
        print("Attempting Gemini API (Stable Version)...")
        genai.configure(api_key=GEMINI_API_KEY)
        
        # FIX: Direct model name without 'models/' prefix
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Safety settings disable ki hain taaki facts block na hon
        response = model.generate_content(
            PROMPT,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        return response.text.strip()
    except Exception as e:
        print(f"Main attempt failed: {e}")
        # Last ditch effort with full path
        try:
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            response = model.generate_content(PROMPT)
            return response.text.strip()
        except Exception as e2:
            print(f"Critical Error: {e2}")
            return None

# Execution logic
text = call_gemini()

if text:
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Success! Script generated in script.txt")
else:
    print("Gemini failed again. Possible invalid API Key or regional restriction.")
    sys.exit(1)
        
