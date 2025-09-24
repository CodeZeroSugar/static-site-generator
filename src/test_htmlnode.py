import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_attributes(self):
        test_prop = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("a", "This is a link for google.com", None, test_prop)

        return node.props_to_html()


if __name__ == "__main__":
    unittest.main()
