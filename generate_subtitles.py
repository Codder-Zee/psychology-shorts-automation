import textwrap

def generate_subs(script, output="subs.txt"):
    lines = textwrap.wrap(script, width=30)
    with open(output, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
