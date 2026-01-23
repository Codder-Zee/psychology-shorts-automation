import requests
import os

API_URL = "https://api-inference.huggingface.co/models/bigscience/bloomz"
headers = {
    "Authorization": f"Bearer {os.environ['HF_TOKEN']}"
}

prompt = (
    "Hindi me 6 scenes wali psychology short video script likho.\n"
    "Har scene 1–2 line ka ho.\n"
    "Topic: human behavior psychology.\n"
    "Tone: suspense + awareness.\n"
    "Total length 40–60 seconds.\n"
    "Har scene alag line me ho."
)

payload = {
    "inputs": prompt,
    "options": {"wait_for_model": True}
}

res = requests.post(API_URL, headers=headers, json=payload)
data = res.json()

text = ""
if isinstance(data, list) and "generated_text" in data[0]:
    text = data[0]["generated_text"]
else:
    text = (
        "Log aksar apni asli feelings chhupa lete hain.\n"
        "Ye habit dheere dheere emotional distance banati hai.\n"
        "Psychology ke mutabik ye self-protection hota hai.\n"
        "Par zyada der tak chup rehna dangerous ho sakta hai.\n"
        "Strong log madad maangne se nahi darte.\n"
        "Isliye bolna seekhna bhi strength hai."
    )

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(text.strip())
