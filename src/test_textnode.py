import unittest


from textnode import TextNode, TextType, text_node_to_html_node
from split_nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from extract_markdown import extract_markdown_images, extract_markdown_links
from markdown_to_blocks import markdown_to_blocks
from block_type import BlockType, block_to_block_type
from markdown_to_html_node import markdown_to_html_node


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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.boot.dev) and here is some text at the end.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and here is some text at the end.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images2(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and here is some text at the end.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and here is some text at the end.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_empty(self):
        node = TextNode(
            "",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [],
            new_nodes,
        )

    def test_split_multiple_link_nodes(self):
        node1 = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.boot.dev) and here is some text at the end.",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.boot.dev) and here is some text at the end.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and here is some text at the end.", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and here is some text at the end.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_to_textnodes1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_heading(self):
        lines = """###### #This is the heading line.
            Here is some more random text below the heading.
            This text is also below the heading."""
        result = block_to_block_type(lines)
        self.assertEqual(
            result,
            BlockType.HEADING,
        )

    def test_block_to_code(self):
        lines = """
        ```.py
        this is some pretend code.
        Here is some more random code text.
        This text is also random code text.
        ```
        """
        result = block_to_block_type(lines)
        self.assertEqual(
            result,
            BlockType.CODE,
        )

    def test_block_to_quote(self):
        lines = """>this is a quote.
            > this is another quote
            >this is another nother quote.
            > this is the last quote line"""
        result = block_to_block_type(lines)
        self.assertEqual(
            result,
            BlockType.QUOTE,
        )

    def test_block_to_unordered(self):
        lines = """- this list is not ordered.
            - this list is unordered 
            - this is a list that is unordered.
            - this is the last list line"""
        result = block_to_block_type(lines)
        self.assertEqual(
            result,
            BlockType.UNORDERED_LIST,
        )

    def test_block_to_ordered(self):
        lines = """1. this list is ordered.
            2. this list is ordered 
            3. this is a list that is ordered.
            4. this is the last list line"""
        result = block_to_block_type(lines)
        self.assertEqual(
            result,
            BlockType.ORDERED_LIST,
        )

    def test_block_to_paragraph(self):
        lines = """This is the paragraph block.
            Here is some more random text in a paragraph.
            This text is also in the paragraph."""
        result = block_to_block_type(lines)
        self.assertEqual(
            result,
            BlockType.PARAGRAPH,
        )

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_h3_inline(self):
        md = "### Hello, **world**"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h3>Hello, <b>world</b></h3></div>",
        )

    def test_heading_h3_inline_no_space(self):
        md = "###Hello, **world**"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h3>Hello, <b>world</b></h3></div>",
        )

    def test_paragraphs_multi_line(self):
        md = """
        This is a **bold** paragraph with some _italic_ text and a [link to Google](https://www.google.com). It also includes 
        some `inline code` for emphasis.
        """
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            '<div><p>This is a <b>bold</b> paragraph with some <i>italic</i> text and a <a href="https://www.google.com">link to Google</a>. It also includes some <code>inline code</code> for emphasis.</p></div>',
        )

    def test_blockquotes(self):
        md = """
            > This is an important quote from a wise person.
            > It spans multiple lines to emphasize its significance.
            """
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is an important quote from a wise person.\nIt spans multiple lines to emphasize its significance.</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
            - Item 1
            - Item 2
            - Item 3
        """
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
            1. This
            2. is
            3. an
            4. ordered
            5. list
        """
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>This</li><li>is</li><li>an</li><li>ordered</li><li>list</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
