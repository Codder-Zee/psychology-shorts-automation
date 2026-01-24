import os
import sys
import google.generativeai as genai

# Step 1: GitHub Secrets se key uthana
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
        
        # FIX: Direct name use kar rahe hain bina kisi prefix ke
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Safety settings ko bypass karna
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
        print(f"Error during API call: {e}")
        return None

# Execution logic
text = call_gemini()

if text:
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("SUCCESS: Script saved in script.txt!")
else:
    print("FAILED: Response generate nahi hua.")
    sys.exit(1)
    
