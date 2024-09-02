import unittest
from inline_markdown import (
    text_to_textnodes,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_delimiter,
    text_node_to_html_node,
)
from htmlnode import LeafNode
from textnode import TextNode


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

# Regular text node
text_node_1 = TextNode("Hello, World!", "text")
# Bold text node
text_node_2 = TextNode("This is bold text", "bold")
# Italic text node
text_node_3 = TextNode("Italicized content", "italic")
# Code text node
text_node_4 = TextNode("print('Hello, World!')", "code")
# Link text node
text_node_5 = TextNode("Click here", "link", url="https://example.com")
# Image text node
text_node_6 = TextNode(
    "Image description", "image", url="https://example.com/image.jpg"
)
# Mixed cases with same types but different texts and urls
text_node_7 = TextNode("Another bold example", "bold")
text_node_8 = TextNode("Click this link", "link", url="https://anotherexample.com")
text_node_9 = TextNode("Sample code snippet", "code")
# Identical to text_node_2 for equality testing
text_node_10 = TextNode("This is bold text", "bold")
# Another identical node for equality testing with a different type
text_node_11 = TextNode("This is bold text", "text")
# Testing different text with image
text_node_12 = TextNode(
    "Different image description",
    "image",
    url="https://example.com/different_image.jpg",
)


class TestInlineMarkDown(unittest.TestCase):
    def test_text_eq(self):
        self.assertEqual(
            text_node_to_html_node(text_node_1).__repr__(),
            "LeafNode(None, Hello, World!, None)",
        )

    def test_text(self):
        node = TextNode("This is a text node", "text")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", "image", "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", "bold")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_split_delimiter(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "`", text_type_code),
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
        )

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("bold", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("italic", text_type_italic),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_image_extractor(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_link_extractor(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with a link ", text_type_text),
                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode(
                    "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_no_links(self):
        node = TextNode("This is plain text without any links.", text_type_text)
        self.assertEqual(
            split_nodes_link([node]),
            [TextNode("This is plain text without any links.", text_type_text)],
        )

    def test_link_at_beginning(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) is a great resource.", text_type_text
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                TextNode(" is a great resource.", text_type_text),
            ],
        )

    def test_link_at_end(self):
        node = TextNode(
            "Check this out: [to boot dev](https://www.boot.dev)", text_type_text
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("Check this out: ", text_type_text),
                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            ],
        )

    def test_multiple_links(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode(
                    "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_consecutive_links(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                TextNode(
                    "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode(
                    "obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_splitnodes_no_assert(self):    
        testing_markdown="""
            # Sample Markdown Document

                    Welcome to this **Markdown** testing document! This is a great place to **test formatting**.

            ## Heading Level 2

                    This is an example of a *heading* and some *italicized text*. You can also use `inline code` to highlight small code snippets.

            ### Heading Level 3

                    Here's an example of an unordered list:
                    - First item
                    - Second item
                    - Third item

                    Now, let's look at an ordered list:
                    1. Step one
                    2. Step two
                    3. Step three

            ### Links and Images

                    Here is a [link to OpenAI](https://openai.com).

                    Here is an image:
                    ![Example Image](https://via.placeholder.com/150)

            ### Blockquote Example

                    > This is a blockquote. Blockquotes are great for quoting text or highlighting ideas.

            ### Code Block Example

                    ```python
                    def hello_world():
                        print("Hello, world!")
                    ```
                    """
        try:
            result = text_to_textnodes(testing_markdown)
            print("Function ran successfully")
            print("Number of blocks:", len(result))
            for i, block in enumerate(result):
                print(f"Block {i + 1}:")
                print(block)
                print("---")
        except Exception as e:
            print("An error occurred:")
            print(str(e))
    
