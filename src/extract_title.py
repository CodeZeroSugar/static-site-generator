def extract_title(markdown):
    lines = (markdown.strip()).split("\n")
    for line in lines:
        line = line.lstrip()
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("error: this file has no heading")
