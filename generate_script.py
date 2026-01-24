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
        [span_6](start_span)[span_7](start_span)print("Error: GEMINI_API_KEY missing in GitHub Secrets")[span_6](end_span)[span_7](end_span)
        return None
    
    try:
        [span_8](start_span)[span_9](start_span)print("Attempting Gemini API (Stable Path)...")[span_8](end_span)[span_9](end_span)
        genai.configure(api_key=GEMINI_API_KEY)
        
        # FIX: Try without 'models/' prefix first
        [span_10](start_span)[span_11](start_span)model = genai.GenerativeModel('gemini-1.5-flash')[span_10](end_span)[span_11](end_span)
        
        # Safety settings ko bypass karna psychology facts ke liye
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
        [span_12](start_span)[span_13](start_span)print(f"First attempt failed: {e}. Trying fallback path...")[span_12](end_span)[span_13](end_span)
        try:
            # Fallback: Agar upar wala fail ho toh 'models/' ke saath try karein
            [span_14](start_span)[span_15](start_span)model = genai.GenerativeModel('models/gemini-1.5-flash')[span_14](end_span)[span_15](end_span)
            response = model.generate_content(PROMPT)
            return response.text.strip()
        except Exception as e2:
            [span_16](start_span)[span_17](start_span)print(f"All attempts failed: {e2}")[span_16](end_span)[span_17](end_span)
            return None

# Execution logic
text = call_gemini()

if text:
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(text)
    [span_18](start_span)[span_19](start_span)print("SUCCESS: Script saved in script.txt!")[span_18](end_span)[span_19](end_span)
else:
    [span_20](start_span)[span_21](start_span)print("FAILED: Gemini response nahi de raha.")[span_20](end_span)[span_21](end_span)
    sys.exit(1)
        
