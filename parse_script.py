import re, os

with open("script.txt", encoding="utf-8") as f:
    data = f.read()

title = re.search(r"Title:(.*)", data).group(1).strip()
script = re.search(r"Script:(.*)Keyword:", data, re.S).group(1).strip()
keywords_raw = re.search(r"Keyword:(.*)", data, re.S).group(1)

keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]

os.makedirs("output", exist_ok=True)

with open("output/title.txt", "w", encoding="utf-8") as f:
    f.write(title)

with open("output/script.txt", "w", encoding="utf-8") as f:
    f.write(script)

with open("output/keywords.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(keywords))

print("Parsed:", title, "| Scenes:", len(keywords))
