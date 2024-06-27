import unittest

from block import block_to_block_type, block_to_htmlnode, markdown_to_blocks
from block import (
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
)
from htmlnode import LeafNode, ParentNode


class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        test_cases = [
            (
                """
                This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
                """,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                    "* This is a list\n* with items",
                ],
            ),
        ]

        for test in test_cases:
            self.assertEqual(markdown_to_blocks(test[0]), test[1])

    def test_block_to_block_type(self):
        test_cases = [
            (
                ">quote1\n>quote2",
                block_type_quote,
            ),
            (
                "```\nline1\nline2```",
                block_type_code,
            ),
            (
                """
                * line1
                - line2
                line3
                """,
                block_type_paragraph,
            ),
            (
                "### heading1\n# heading 2",
                block_type_heading,
            ),
        ]

        for test in test_cases:
            self.assertEqual(block_to_block_type(test[0]), test[1])

    def test_block_to_htmlnode(self):
        test_cases = [
            (
                "# h1 heading\ntext with *italic*",
                block_type_heading,
                ParentNode(
                    tag="h1",
                    children=[
                        LeafNode(tag=None, value="h1 heading\ntext with "),
                        LeafNode(tag="i", value="italic"),
                    ],
                ),
            ),
            (
                "```code comes here\nand here\n and even here```",
                block_type_code,
                ParentNode(
                    tag="pre",
                    children=[
                        ParentNode(
                            tag="code",
                            children=[
                                LeafNode(
                                    tag=None,
                                    value="code comes here\nand here\n and even here",
                                )
                            ],
                        )
                    ],
                ),
            ),
            (
                ">first quote\n>second quote\n>third quote",
                block_type_quote,
                ParentNode(
                    tag="blockquote",
                    children=[
                        LeafNode(
                            tag=None, value="first quote\nsecond quote\nthird quote"
                        )
                    ],
                ),
            ),
            (
                "1. first list item\n2. second list item with *italic*\n3. third list item",
                block_type_ordered_list,
                ParentNode(
                    tag="ol",
                    children=[
                        ParentNode(
                            tag="li",
                            children=[LeafNode(tag=None, value="first list item")],
                        ),
                        ParentNode(
                            tag="li",
                            children=[
                                LeafNode(tag=None, value="second list item with "),
                                LeafNode(tag="i", value="italic"),
                            ],
                        ),
                        ParentNode(
                            tag="li",
                            children=[LeafNode(tag=None, value="third list item")],
                        ),
                    ],
                ),
            ),
            (
                "* first list item\n- second list item",
                block_type_unordered_list,
                ParentNode(
                    tag="ul",
                    children=[
                        ParentNode(
                            tag="li",
                            children=[LeafNode(tag=None, value="first list item")],
                        ),
                        ParentNode(
                            tag="li",
                            children=[LeafNode(tag=None, value="second list item")],
                        ),
                    ],
                ),
            ),
            (
                "**bold text** with regular text\n and also a bit of `code` and *italic*",
                block_type_paragraph,
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(tag="b", value="bold text"),
                        LeafNode(
                            tag=None, value=" with regular text\n and also a bit of "
                        ),
                        LeafNode(tag="code", value="code"),
                        LeafNode(tag=None, value=" and "),
                        LeafNode(tag="i", value="italic"),
                    ],
                ),
            ),
        ]

        for test in test_cases:
            self.assertEqual(block_to_htmlnode(test[0], test[1]), test[2])

        with self.assertRaises(Exception) as context:
            block_to_htmlnode("some text", "spin")

        self.assertEqual(str(context.exception), "invalid block type provided")


if __name__ == "__main__":
    unittest.main()
