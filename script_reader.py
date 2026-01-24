def read_next_script(path="script.txt"):
    with open(path, "r", encoding="utf-8") as f:
        data = f.read().strip()

    if not data:
        raise Exception("No script found")

    blocks = data.split("\n\nTitle:")
    block = blocks[0] if data.startswith("Title:") else "Title:" + blocks[1]

    title = block.split("Title:")[1].split("Script:")[0].strip()
    script = block.split("Script:")[1].split("Keyword:")[0].strip()
    keywords_raw = block.split("Keyword:")[1].strip()
    keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]

    remaining = "\n\nTitle:".join(blocks[1:])
    with open(path, "w", encoding="utf-8") as f:
        f.write(remaining.strip())

    return title, script, keywords
