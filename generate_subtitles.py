import textwrap

text = open("script.txt", encoding="utf-8").read()

lines = textwrap.wrap(text, width=25)

with open("subs.txt", "w", encoding="utf-8") as f:
    for line in lines[:6]:  # Shorts ke liye enough
        f.write(line + "\n")
