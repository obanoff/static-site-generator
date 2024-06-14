import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "here should be link",
            None,
            {"href": "https://boot.dev", "id": "link"},
        )
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev" id="link"')


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node1 = LeafNode("p", "Just a paragraph in italic", {"style": "font-style: italic;"})
        node2 = LeafNode("a", "Just a link", {"href": "https://google.com", "id": "link"})
        self.assertEqual(node1.to_html(), '<p style="font-style: italic;">Just a paragraph in italic</p>')
        self.assertEqual(node2.to_html(), '<a href="https://google.com" id="link">Just a link</a>')


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node1 = ParentNode("p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node2 = ParentNode(
            "div",
            [
                ParentNode("div", [
                    LeafNode("p", "Paragraph in bold", {"style": "font-weight: bold;"}),
                    LeafNode("a", "A link", {"href": "https://google.com"})
                ], {"id": "secondary-div"})
            ]
            , {"class": "main-div"})

        self.assertEqual(node1.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        self.assertEqual(node2.to_html(), '<div class="main-div"><div id="secondary-div"><p style="font-weight: bold;">Paragraph in bold</p><a href="https://google.com">A link</a></div></div>')


        

if __name__ == "__main__":
    unittest.main()


