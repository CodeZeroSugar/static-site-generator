import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.LINK)
        return node

    def test_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        return node

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "www.fakeurl.com")
        return node


if __name__ == "__main__":
    unittest.main()
