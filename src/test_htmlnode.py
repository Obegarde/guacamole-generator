import unittest
from htmlnode import ParentNode, LeafNode, HTMLNode



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
        
    def test_rec_to_html(self):        
        node = ParentNode("p",[LeafNode("b", "Bold text"),LeafNode(None, "Normal text"),LeafNode("i", "italic text"),LeafNode(None, "Normal text"),],)
        self.assertEqual(node.to_html(),"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    
    
    def test_rec_to_html2(self):        
        node = ParentNode("p",[LeafNode("b", "Bold text"),LeafNode(None, "Normal text"),LeafNode("i", "italic text"),LeafNode(None, "Normal text"),],)
        self.assertNotEqual(node.to_html(),"<p><b>Bold text</>Normal text<i>italic text</i>Normal text</p>")


    def test_rec_to_html_with_nested_tags(self):
        node = ParentNode("div", [
            ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")]),
            ParentNode("span", [LeafNode("i", "Italic text"), LeafNode(None, "More normal text")]),
        ])
        self.assertEqual(node.to_html(), "<div><p><b>Bold text</b>Normal text</p><span><i>Italic text</i>More normal text</span></div>")

    def test_rec_to_html_empty_parent(self):
        node = ParentNode("p", [])
        self.assertEqual(node.to_html(), "<p></p>")

    def test_rec_to_html_empty_leaf(self):
        node = ParentNode("p", [LeafNode("b", ""), LeafNode(None, "Normal text")])
        self.assertEqual(node.to_html(), "<p><b></b>Normal text</p>")

    def test_rec_to_html_self_closing_tag(self):
        node = ParentNode("img", [])
        self.assertNotEqual(node.to_html(), "<img />")

    def test_rec_to_html_mismatched_tags(self):
        node = ParentNode("div", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")])
        self.assertNotEqual(node.to_html(), "<div><b>Bold text</>Normal text</div>")

    def test_rec_to_html_incomplete_tag(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")])
        self.assertNotEqual(node.to_html(), "<p><b>Bold textNormal text</b></p>")

    def test_rec_to_html_single_leaf(self):
        node = ParentNode("h1", [LeafNode(None, "Header Text")])
        self.assertEqual(node.to_html(), "<h1>Header Text</h1>")

    def test_rec_to_html_with_multiple_nodes_and_no_tags(self):
        node = ParentNode("p", [LeafNode(None, "Text1"), LeafNode(None, "Text2"), LeafNode(None, "Text3")])
        self.assertEqual(node.to_html(), "<p>Text1Text2Text3</p>")

    def test_rec_to_html_with_complex_nesting(self):
        node = ParentNode("div", [
            ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "Item 1")]),
                ParentNode("li", [LeafNode(None, "Item 2")]),
            ]),
            LeafNode("p", "End of list")
        ])
        self.assertEqual(node.to_html(), "<div><ul><li>Item 1</li><li>Item 2</li></ul><p>End of list</p></div>")

    def test_rec_to_html_malformed_html(self):
        node = ParentNode("div", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")])
        self.assertNotEqual(node.to_html(), "<div><b>Bold text<b>Normal text</div>")


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

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()
