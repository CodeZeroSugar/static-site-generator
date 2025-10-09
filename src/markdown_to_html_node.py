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


def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    children_nodes = []
    for block in block_list:
        current_block_type = block_to_block_type(block)
        match current_block_type:
            case BlockType.PARAGRAPH:
                clean_block = block.strip()
                children = text_to_children(clean_block)
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
                block_lines = block.split("\n")
                remove_ticks = block_lines[1:-1]
                clean_block = "\n".join(remove_ticks) + "\n"
                node = ParentNode("pre", [LeafNode("code", clean_block)])
                children_nodes.append(node)

            case BlockType.QUOTE:
                quote_lines = block.split("\n")
                clean_lines = []
                for line in quote_lines:
                    if line.startswith("> "):
                        clean_lines.append(line[2:])
                    elif line.startswith(">"):
                        clean_lines.append(line[1:])
                    else:
                        clean_lines.append(line)
                clean_block = "\n".join(clean_lines)
                children = text_to_children(clean_block)
                node = ParentNode("blockquote", children)
                children_nodes.append(node)

            case BlockType.UNORDERED_LIST:
                li_nodes = []
                for line in block.split("\n"):
                    if not line.strip():
                        continue
                    if line.startswith(("- ", "* ")):
                        item = line[2:]
                    else:
                        item = line
                    children = text_to_children(item)

                    li_nodes.append(ParentNode("li", children))

                node = ParentNode("ul", li_nodes)
                children_nodes.append(node)

            case BlockType.ORDERED_LIST:
                pass

    return (
        ParentNode("div", children_nodes)
        if len(children_nodes) > 0
        else ParentNode("div", None)
    )
