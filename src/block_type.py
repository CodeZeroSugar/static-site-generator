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
    while i < len(line) and i < 6 and line[i] == "#":
        i += 1
    return i > 0 and (i < len(line))


def block_to_block_type(block):
    lines = block.split("\n")
    start = 0
    while start < len(lines) and not lines[start].strip():
        start += 1
    end = len(lines) - 1
    while end >= 0 and not lines[end].strip():
        end -= 1

    if (
        end - start >= 2
        and lines[start].strip().startswith("```")
        and lines[end].strip().startswith("```")
    ):
        return BlockType.CODE

    if is_heading(lines[0]):
        return BlockType.HEADING

    lines_norm = [ln for ln in lines if ln.strip()]
    if lines_norm and all(ln.lstrip().startswith(">") for ln in lines_norm):
        return BlockType.QUOTE

    if lines_norm and all(ln.lstrip().startswith("-") for ln in lines_norm):
        return BlockType.UNORDERED_LIST

    nonempty = [ln for ln in lines if ln.strip()]
    if nonempty and all(
        ln.lstrip().split(".", 1)[0].isdigit()
        and ln.lstrip().startswith(f"{ln.lstrip().split('.', 1)[0]}. ")
        for ln in nonempty
    ):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
