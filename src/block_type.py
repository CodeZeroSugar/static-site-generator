from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def is_heading(line):
    i = 0
    char = line[0]
    while char == "#":
        i += 1
        char = line[i]
    if char == " " and 1 <= i <= 6:
        return True
    return False


def block_to_block_type(block):
    lines = block.split("\n")
    if (
        lines[0].lstrip().startswith("```")
        and lines[-1].lstrip().startswith("```")
        and len(lines) >= 3
    ):
        return BlockType.CODE

    if is_heading(lines[0]):
        return BlockType.HEADING

    if all(line.lstrip().startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.lstrip().startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    order_test = True
    for index, line in enumerate(lines, start=1):
        if not line.lstrip().startswith(f"{index}. "):
            order_test = False
            break
    if order_test:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
