import requests
import os
import time

API_URL = "https://api-inference.huggingface.co/models/bigscience/bloomz"
headers = {
    "Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"
}

prompt = (
    "Hindi me 25-30 shabdon ka psychology fact likho "
    "jo human behavior par ho, awareness tone me."
)

payload = {
    "inputs": prompt,
    "options": {
        "wait_for_model": True
    }
}

response = requests.post(API_URL, headers=headers, json=payload)
data = response.json()

# 🔐 SAFE handling
text = ""

if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
    text = data[0]["generated_text"]
elif isinstance(data, dict) and "generated_text" in data:
    text = data["generated_text"]
else:
    # fallback (VERY IMPORTANT)
    text = (
        "Psychology ke mutabik agar koi vyakti baar baar chup ho jaata hai, "
        "to wo apni emotions ko control kar raha hota hai."
    )

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(text.strip())
