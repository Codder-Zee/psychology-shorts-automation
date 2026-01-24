import textwrap
import os

if os.path.exists("script.txt"):
    text = open("script.txt", encoding="utf-8").read()
    lines = textwrap.wrap(text, width=30)

    with open("subs.txt", "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    print("Subtitles generated in subs.txt")
  
