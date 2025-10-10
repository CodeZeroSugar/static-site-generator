from htmlnode import LeafNode, ParentNode
from markdown_to_blocks import markdown_to_blocks
from block_type import BlockType, block_to_block_type
from textnode import text_node_to_html_node
from split_nodes import text_to_textnodes


def text_to_children(text):
    return [text_node_to_html_node(n) for n in text_to_textnodes(text)]


def heading_level(text):
    i = 0
    while i < len(text) and i < 6 and text[i] == "#":
        i += 1
    return i


def check_for_int(text):
    i = 0
    while i < len(text) and text[i].isdigit():
        i += 1
    return i


def stip_order_prefix(line):
    i = check_for_int(line)
    if i > 0 and i + 1 < len(line) and line[i] == "." and line[i + 1] == " ":
        return line[i + 2 :]
    return line


def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    children_nodes = []
    for block in block_list:
        current_block_type = block_to_block_type(block)
        match current_block_type:
            case BlockType.PARAGRAPH:
                lines = [ln.strip() for ln in block.split("\n") if ln.strip()]
                clean = " ".join(lines)
                children = text_to_children(clean)
                p_node = ParentNode("p", children)
                children_nodes.append(p_node)

            case BlockType.HEADING:
                first_line = block.split("\n", 1)[0]
                level = heading_level(first_line)
                content = first_line[level:].lstrip()
                children = text_to_children(content)
                node = ParentNode(f"h{level}", children)
                children_nodes.append(node)

            case BlockType.CODE:
                lines = block.split("\n")
                start = 0
                while start < len(lines) and not lines[start].strip():
                    start += 1
                end = len(lines) - 1
                while end >= 0 and not lines[end].strip():
                    end -= 1
                inner = lines[start + 1 : end]

                while inner and not inner[0].strip():
                    inner.pop(0)
                while inner and not inner[-1].strip():
                    inner.pop()

                indents = [len(l) - len(l.lstrip(" ")) for l in inner if l.strip()]
                common = min(indents) if indents else 0
                dedented = [(l[common:] if l.strip() else "") for l in inner]

                clean = "\n".join(dedented)
                if clean and not clean.endswith("\n"):
                    clean += "\n"

                children_nodes.append(ParentNode("pre", [LeafNode("code", clean)]))

            case BlockType.QUOTE:
                quote_lines = block.split("\n")
                clean_lines = []
                for line in quote_lines:
                    s = line.lstrip()
                    if s.startswith("> "):
                        clean_lines.append(s[2:])
                    elif s.startswith(">"):
                        clean_lines.append(s[1:])
                    else:
                        clean_lines.append(s)
                clean_block = "\n".join(clean_lines).strip()
                children = text_to_children(clean_block)
                node = ParentNode("blockquote", children)
                children_nodes.append(node)

            case BlockType.UNORDERED_LIST:
                li_nodes = []
                for line in block.split("\n"):
                    if not line.strip():
                        continue
                    if line.lstrip().startswith(("- ", "* ")):
                        item = line.lstrip()[2:]
                    else:
                        item = line
                    children = text_to_children(item)

                    li_nodes.append(ParentNode("li", children))

                node = ParentNode("ul", li_nodes)
                children_nodes.append(node)

            case BlockType.ORDERED_LIST:
                li_nodes = []
                for line in block.split("\n"):
                    if not line.strip():
                        continue
                    item = stip_order_prefix(line.lstrip())
                    li_nodes.append(ParentNode("li", text_to_children(item)))

                node = ParentNode("ol", li_nodes)
                children_nodes.append(node)

    return (
        ParentNode("div", children_nodes)
        if len(children_nodes) > 0
        else ParentNode("div", None)
    )
