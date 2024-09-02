import unittest
from markdown_html import markdown_to_html_node, extract_title 
from block_markdown import block_to_block_type

class TestMarkdownToHTML(unittest.TestCase):
    def test_extract_title(self):       
        markdown="""
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
        self.assertEqual(extract_title(markdown),"Sample Markdown Document")



def test_paragraph(self):
                md = """
This is **bolded** paragraph
text in a p
tag here

"""

                node = markdown_to_html_node(md)
                html = node.to_html()
                self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )