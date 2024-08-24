import unittest
from htmlnode import LeafNode, HTMLNode



node6 = HTMLNode("li", "Item 1", [], {})
node7 = HTMLNode("li", "Item 2", [], {})
node8 = HTMLNode("li", "Item 3", [], {})

node5 = HTMLNode("ul", "", [node6, node7, node8], {"class": "item-list"})

node4 = HTMLNode("a", "Click here to learn more", [], {"href": "https://www.example.com", "target": "_blank"})
node3 = HTMLNode("p", "This is a paragraph introducing the content of the page.", [], {"class": "intro"})
node2 = HTMLNode("h1", "Welcome to My Website", [], {"class": "header", "id": "main-title"})

node1 = HTMLNode("div", "", [node2, node3, node4, node5], {"class": "container"})

node9 = HTMLNode("footer", "© 2024 My Website", [], {"class": "footer"})


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        with self.assertRaises(NotImplementedError):
            node1.to_html()

    def test_props_to_html(self):
        self.assertEqual(node9.props_to_html()," class=\"footer\"")
        
    def test_props_to_html2(self):
        self.assertEqual(node4.props_to_html()," href=\"https://www.example.com\" target=\"_blank\"")

    def test_props_to_htmlNot(self):
        self.assertNotEqual(node2.props_to_html()," class=header id=maintitle")

    def test_repr(self):
        self.assertEqual(repr(node6),"HTMLNode(li, Item 1, [], {})")

 





    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_leafnode_to_html(self):
        self.assertEqual(LeafNode("p","This is a paragraph of text.").to_html(),"<p>This is a paragraph of text.</p>")

    def test_leafnode_to_html2(self):
        self.assertEqual(LeafNode("a","Click Me!",{"href": "https://www.google.com"}).to_html(),'<a href="https://www.google.com">Click Me!</a>')

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
        

if __name__ == "__main__":
    unittest.main()
