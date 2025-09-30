from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) % 2 != 0:
            raise Exception(
                f"Closing delimiter for {delimiter} not found. Invalid Markdown syntax"
            )

        split_node_text = node.text.split(delimiter)

        new_node = []
        for i in range(0, len(split_node_text)):
            if i % 2 == 0:
                new_node.append(TextNode(split_node_text[i], TextType.TEXT))
            else:
                new_node.append(TextNode(split_node_text[i], text_type))

        new_nodes.extend(new_node)

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        if node_text == "":
            continue

        matches = extract_markdown_images(node_text)

        if len(matches) == 0:
            new_nodes.append(node)
            continue

        for match in matches:
            sections = node_text.split(f"![{match[0]}]({match[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    match[0],
                    TextType.IMAGE,
                    match[1],
                )
            )
            node_text = sections[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        node_text = node.text
        if node_text == "":
            continue

        matches = extract_markdown_links(node_text)

        if len(matches) == 0:
            new_nodes.append(node)
            continue

        for match in matches:
            sections = node_text.split(f"[{match[0]}]({match[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    match[0],
                    TextType.LINK,
                    match[1],
                )
            )
            node_text = sections[1]

        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    current_nodes = [
        TextNode(
            text,
            TextType.TEXT,
        )
    ]
    current_nodes = split_nodes_delimiter(current_nodes, "`", TextType.CODE)
    current_nodes = split_nodes_delimiter(current_nodes, "**", TextType.BOLD)
    current_nodes = split_nodes_delimiter(current_nodes, "_", TextType.ITALIC)
    current_nodes = split_nodes_link(current_nodes)
    current_nodes = split_nodes_image(current_nodes)
    return current_nodes
