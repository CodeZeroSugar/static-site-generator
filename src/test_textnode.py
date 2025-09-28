import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from split_nodes_delimiter import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_false1(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.LINK)
        return node

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, TextType.TEXT, https://www.boot.dev)",
            repr(node),
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode(
            "This is a link node", TextType.LINK, "https://www.linknode.com"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.linknode.com"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "url/of/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "url/of/image.jpg", "alt": "This is an image node"}
        )

    def test_bold_split(self):
        node = TextNode("This is text with **bold text**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with ", TextType.TEXT, None),
                TextNode("bold text", TextType.BOLD, None),
                TextNode("", TextType.TEXT, None),
            ],
        )

    def test_italic_split(self):
        node = TextNode("Look there, _some italic text_! Wow so cool!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Look there, ", TextType.TEXT, None),
                TextNode("some italic text", TextType.ITALIC, None),
                TextNode("! Wow so cool!", TextType.TEXT, None),
            ],
        )

    def test_code_split(self):
        node = TextNode(
            "Here's `some code`. Here's `more code`. Oh look, there's `some more code` here.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Here's ", TextType.TEXT, None),
                TextNode("some code", TextType.CODE, None),
                TextNode(". Here's ", TextType.TEXT, None),
                TextNode("more code", TextType.CODE, None),
                TextNode(". Oh look, there's ", TextType.TEXT, None),
                TextNode("some more code", TextType.CODE, None),
                TextNode(" here.", TextType.TEXT),
            ],
        )

    def test_multiple_split(self):
        node1 = TextNode("Look there, _some italic text_! Wow so cool!", TextType.TEXT)
        node2 = TextNode("Look there, _some italic text_! Wow so cool!", TextType.TEXT)
        node3 = TextNode("Look there, _some italic text_! Wow so cool!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Look there, ", TextType.TEXT, None),
                TextNode("some italic text", TextType.ITALIC, None),
                TextNode("! Wow so cool!", TextType.TEXT, None),
                TextNode("Look there, ", TextType.TEXT, None),
                TextNode("some italic text", TextType.ITALIC, None),
                TextNode("! Wow so cool!", TextType.TEXT, None),
                TextNode("Look there, ", TextType.TEXT, None),
                TextNode("some italic text", TextType.ITALIC, None),
                TextNode("! Wow so cool!", TextType.TEXT, None),
            ],
        )

    def test_missing_delimiter(self):
        node = TextNode("This **string should be bold", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)


if __name__ == "__main__":
    unittest.main()
