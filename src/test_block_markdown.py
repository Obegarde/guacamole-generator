import unittest
from block_markdown import markdown_to_blocks, block_to_block_type
from constants import block_type_paragraph,block_type_olist,block_type_ulist,block_type_quote,block_type_code,block_type_heading

class TestBlockMarkDown(unittest.TestCase):
    def test_block_markdown(self):
        text = """# This is a heading

    This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    * This is the first list item in a list block
    * This is a list item
    * This is another list item"""

        self.assertListEqual(
            markdown_to_blocks(text),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block
    * This is a list item
    * This is another list item""",
            ],
        )

    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

    This is another paragraph with *italic* text and `code` here
    This is the same paragraph on a new line

    * This is a list
    * with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,[
                "This is **bolded** paragraph",
                """This is another paragraph with *italic* text and `code` here
    This is the same paragraph on a new line""",
                """* This is a list
    * with items""",],)

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )


    def test_headers(self):
        self.assertEqual(block_to_block_type('###### Header 6'), block_type_heading)
        self.assertEqual(block_to_block_type('##### Header 5'), block_type_heading)
        self.assertEqual(block_to_block_type('#### Header 4'), block_type_heading)
        self.assertEqual(block_to_block_type('### Header 3'), block_type_heading)
        self.assertEqual(block_to_block_type('## Header 2'), block_type_heading)
        self.assertEqual(block_to_block_type('# Header 1'), block_type_heading)
        
   
   
  

    def test_quote(self):
        self.assertEqual(block_to_block_type('> This is a quote'), block_type_quote)
        self.assertEqual(block_to_block_type('> Another quote block'), block_type_quote)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type('* Item in list'), block_type_ulist)
        self.assertEqual(block_to_block_type('- Another item'), block_type_ulist)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type('1. First item'), block_type_olist)
        self.assertEqual(block_to_block_type('123. Another item'), block_type_paragraph)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type('Just a normal paragraph.'), block_type_paragraph)
        self.assertEqual(block_to_block_type('No special formatting here.'), block_type_paragraph)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_ulist)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_olist)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)
