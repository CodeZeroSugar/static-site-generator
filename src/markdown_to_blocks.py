def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        if not block.strip():
            continue
        cleaned_blocks.append(block.strip("\n"))
    return cleaned_blocks
