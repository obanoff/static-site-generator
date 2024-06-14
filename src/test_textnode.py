import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertEqual(node, node2)


    def test_eq_false(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)


    def test_eq_false2(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node2", text_type_text)
        self.assertNotEqual(node, node2)


    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_italic, "https://www.boot.dev")
        node2 = TextNode(
            "This is a text node", text_type_italic, "https://www.boot.dev"
        )
        self.assertEqual(node, node2)


    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


    def test_split_nodes_delimiter(self):
        test_cases = [
            ([TextNode("This is text with a `code block` word", text_type_text)], "`", text_type_code, [
                TextNode("This is text with a ", text_type_text, None),
                TextNode("`code block`", text_type_code, None),
                TextNode(" word", text_type_text, None),
            ]),
            ([
                TextNode("*This is italic text* and **bold not included**", text_type_text), 
                TextNode("Partly *italic*", text_type_code), 
                TextNode("*full italic*", text_type_italic)
            ], "*", text_type_italic,[
                 TextNode("*This is italic text*", text_type_italic),
                 TextNode(" and **bold not included**", text_type_text),
                 TextNode("Partly ", text_type_text),
                 TextNode("*italic*", text_type_italic),
                 TextNode("*full italic*", text_type_italic)
             ]),
            ([
                TextNode("Text **bold** and **bold again**", text_type_text)
            ], "**", text_type_bold, [
                TextNode("Text ", text_type_text),
                TextNode("**bold**", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("**bold again**", text_type_bold)
             ] ),
            ([
                TextNode("Text **bold** and *italic is not included* here!", text_type_text)
            ], "**", text_type_bold, [
                TextNode("Text ", text_type_text),
                TextNode("**bold**", text_type_bold),
                TextNode(" and *italic is not included* here!", text_type_text),
             ] ),
        ]

        for test in test_cases:
            self.assertEqual(split_nodes_delimiter(test[0], test[1], test[2]), test[3])



    def test_extract_markdown_images(self):
        images = [
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)",
        ]

        for img in images:
            self.assertEqual(extract_markdown_images(img), [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])


    def test_extract_markdown_links(self):
        links = [
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
        ]

        for link in links:
            self.assertEqual(extract_markdown_links(link), [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])



if __name__ == "__main__":
    unittest.main()




