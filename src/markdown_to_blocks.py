def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        if block == "":
            del blocks[block]
            continue
        cleaned_blocks.append(block.strip())
    return cleaned_blocks
