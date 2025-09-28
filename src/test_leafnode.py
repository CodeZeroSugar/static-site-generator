import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_b(self):
        node = LeafNode("i", "italic")
        self.assertEqual(node.to_html(), "<i>italic</i>")

    def test_leaf_to_html_tagless(self):
        node = LeafNode(None, "This is a string of raw text")
        self.assertEqual(node.to_html(), "This is a string of raw text")

    def test_repr(self):
        node = LeafNode(
            "p",
            "What a strange world",
            {"class": "primary"},
        )

        self.assertEqual(
            node.__repr__(),
            "LeafNode(p, What a strange world, {'class': 'primary'})",
        )


if __name__ == "__main__":
    unittest.main()
