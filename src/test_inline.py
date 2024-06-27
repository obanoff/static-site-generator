import unittest

from inline import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


class TestInline(unittest.TestCase):

    def test_split_nodes_delimiter(self):
        test_cases = [
            (
                [TextNode("This is text with a `code block` word", text_type_text)],
                "`",
                text_type_code,
                [
                    TextNode("This is text with a ", text_type_text, None),
                    TextNode("code block", text_type_code, None),
                    TextNode(" word", text_type_text, None),
                ],
            ),
            (
                [
                    TextNode(
                        "*This is italic text* and **bold not included**",
                        text_type_text,
                    ),
                    TextNode("Partly *italic*", text_type_code),
                    TextNode("*full italic*", text_type_italic),
                ],
                "*",
                text_type_italic,
                [
                    TextNode("This is italic text", text_type_italic),
                    TextNode(" and **bold not included**", text_type_text),
                    TextNode("Partly ", text_type_text),
                    TextNode("italic", text_type_italic),
                    TextNode("full italic", text_type_italic),
                ],
            ),
            (
                [TextNode("Text **bold** and **bold again**", text_type_text)],
                "**",
                text_type_bold,
                [
                    TextNode("Text ", text_type_text),
                    TextNode("bold", text_type_bold),
                    TextNode(" and ", text_type_text),
                    TextNode("bold again", text_type_bold),
                ],
            ),
            (
                [
                    TextNode(
                        "Text **bold** and *italic is not included* here!",
                        text_type_text,
                    )
                ],
                "**",
                text_type_bold,
                [
                    TextNode("Text ", text_type_text),
                    TextNode("bold", text_type_bold),
                    TextNode(" and *italic is not included* here!", text_type_text),
                ],
            ),
        ]

        for test in test_cases:
            self.assertEqual(split_nodes_delimiter(test[0], test[1], test[2]), test[3])

    def test_extract_markdown_images(self):
        images = [
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)",
        ]

        for img in images:
            self.assertEqual(
                extract_markdown_images(img),
                [
                    (
                        "image",
                        "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                    ),
                    (
                        "another",
                        "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                    ),
                ],
            )

    def test_extract_markdown_links(self):
        links = [
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
        ]

        for link in links:
            self.assertEqual(
                extract_markdown_links(link),
                [
                    ("link", "https://www.example.com"),
                    ("another", "https://www.example.com/another"),
                ],
            )

    def test_splitnodes_image(self):
        test_cases = [
            (
                [
                    TextNode(
                        "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                        text_type_text,
                    )
                ],
                [
                    TextNode("This is text with an ", text_type_text),
                    TextNode(
                        "image",
                        text_type_image,
                        "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                    ),
                    TextNode(" and another ", text_type_text),
                    TextNode(
                        "second image",
                        text_type_image,
                        "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
                    ),
                ],
            ),
            (
                [
                    TextNode(
                        "![image1](https://link1.com)![image2](https://link2.com)",
                        text_type_text,
                    ),
                    TextNode("image3", text_type_image, "https://link3.com"),
                    TextNode("just plain text", text_type_text),
                ],
                [
                    TextNode("image1", text_type_image, "https://link1.com"),
                    TextNode("image2", text_type_image, "https://link2.com"),
                    TextNode("image3", text_type_image, "https://link3.com"),
                    TextNode("just plain text", text_type_text),
                ],
            ),
        ]

        for test in test_cases:
            self.assertEqual(split_nodes_image(test[0]), test[1])

    def test_splitnodes_link(self):
        test_cases = [
            (
                [TextNode("Some text [link1](https://link1.com)", text_type_text)],
                [
                    TextNode("Some text ", text_type_text),
                    TextNode("link1", text_type_link, "https://link1.com"),
                ],
            ),
            (
                [
                    TextNode(
                        "[link1](https://link1.com)[link2](https://link2.com)",
                        text_type_text,
                    ),
                    TextNode("just plain text", text_type_text),
                    TextNode("link3", text_type_link, "https://link3.com"),
                ],
                [
                    TextNode("link1", text_type_link, "https://link1.com"),
                    TextNode("link2", text_type_link, "https://link2.com"),
                    TextNode("just plain text", text_type_text),
                    TextNode("link3", text_type_link, "https://link3.com"),
                ],
            ),
        ]

        for test in test_cases:
            self.assertEqual(split_nodes_link(test[0]), test[1])

    def test_text_to_textnodes(self):
        test_cases = [
            (
                "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)",
                [
                    TextNode("This is ", text_type_text),
                    TextNode("text", text_type_bold),
                    TextNode(" with an ", text_type_text),
                    TextNode("italic", text_type_italic),
                    TextNode(" word and a ", text_type_text),
                    TextNode("code block", text_type_code),
                    TextNode(" and an ", text_type_text),
                    TextNode(
                        "image",
                        text_type_image,
                        "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                    ),
                    TextNode(" and a ", text_type_text),
                    TextNode("link", text_type_link, "https://boot.dev"),
                ],
            ),
            (
                "**bold***italic*![image](https://link-to_image.com) just a plain text",
                [
                    TextNode("bold", text_type_bold),
                    TextNode("italic", text_type_italic),
                    TextNode("image", text_type_image, "https://link-to_image.com"),
                    TextNode(" just a plain text", text_type_text),
                ],
            ),
        ]

        for test in test_cases:
            self.assertEqual(text_to_textnodes(test[0]), test[1])


if __name__ == "__main__":
    unittest.main()
