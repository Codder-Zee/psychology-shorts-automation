import requests, os

API_URL = "https://api-inference.huggingface.co/models/bigscience/bloomz"
headers = {
    "Authorization": f"Bearer {os.environ['HF_TOKEN']}"
}

prompt = (
    "Hindi me 25–30 shabdon ka psychology fact likho, "
    "jo human behavior par ho, awareness tone me."
)

res = requests.post(API_URL, headers=headers, json={"inputs": prompt})
data = res.json()

text = data[0]["generated_text"]

with open("script.txt", "w", encoding="utf-8") as f:
    f.write(text)
