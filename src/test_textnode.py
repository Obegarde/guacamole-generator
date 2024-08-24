import unittest
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)




class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertEqual(node, node2)   
    
    def test_eq_false(self):
        node3 = TextNode("This is not a text node", text_type_bold)
        node4 = TextNode("This is a text node", text_type_text)
        self.assertNotEqual(node3,node4)
    
    def test_eq_url(self):
        node5 = TextNode("123",text_type_text,"www.google.com")
        node6 = TextNode("123",text_type_text,"www.google.com")
        self.assertEqual(node5,node6)
    
    def test_eq_url_false(self):
        node7 = ("123", text_type_text,"www.google.com")
        node8 = ("123", text_type_text,"www.yahoo.com")
        self.assertNotEqual(node7,node8)

    def test_repr(self):
        node = TextNode("This is true", text_type_text,"www.google.com")
        self.assertEqual("TextNode(This is true, text, www.google.com)", repr(node))

    def test_repr_false(self):
        node = TextNode("This is true", text_type_text,"www.google.com")
        self.assertNotEqual("TextNode(This is false, text, www.google.com)", repr(node))
if __name__ == "__main__":
    unittest.main()
