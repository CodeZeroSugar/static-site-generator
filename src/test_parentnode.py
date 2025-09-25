import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_many_children(self):
        child_node_1 = LeafNode("b", "bold child")
        child_node_2 = LeafNode("i", "italics child")
        child_node_3 = LeafNode(
            "a", "link child", {"href": "https://www.linkchild.com"}
        )
        parent_node = ParentNode("p", [child_node_1, child_node_2, child_node_3])
        self.assertEqual(
            parent_node.to_html(),
            '<p><b>bold child</b><i>italics child</i><a href="https://www.linkchild.com">link child</a></p>',
        )
