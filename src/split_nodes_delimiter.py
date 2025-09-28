from textnode import TextNode, TextType


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
