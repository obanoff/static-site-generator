import re

from htmlnode import HTMLNode, ParentNode, LeafNode
from inline import text_to_textnodes
from textnode import TextNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    return list(
        map(lambda x: x.strip(), filter(lambda x: x != "", markdown.split("\n\n")))
    )


def block_to_block_type(block):
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return block_type_heading
    if block.startswith("```") and block.endswith("```"):
        return block_type_code

    lines = block.split("\n")
    for index, line in enumerate(lines):
        if lines[0].startswith(">"):
            if not line.startswith(">"):
                break
            if index == len(lines) - 1:
                return block_type_quote

        if lines[0].startswith("* ") or lines[0].startswith("- "):
            if not (line.startswith("* ") or line.startswith("- ")):
                break
            if index == len(lines) - 1:
                return block_type_unordered_list

        if lines[0].startswith("1. "):
            if not line.startswith(f"{index+1}. "):
                break
            if index == len(lines) - 1:
                return block_type_ordered_list

    return block_type_paragraph


def block_to_htmlnode(block, block_type):
    if block_type not in [
        block_type_heading,
        block_type_code,
        block_type_quote,
        block_type_ordered_list,
        block_type_unordered_list,
        block_type_paragraph,
    ]:
        raise Exception("invalid block type provided")

    children = []

    if block_type == block_type_heading:
        pattern = r"^(#+)?"
        match = re.search(pattern, block)

        if match:
            l = len(match.group())
            if l + 1 >= len(block):
                raise Exception("invalid heading format: empty heading")

            children = list(
                map(
                    lambda x: x.text_node_to_html_node(),
                    text_to_textnodes(block[l + 1 :]),
                )
            )

            return ParentNode(tag=f"h{l}", children=children)
        else:
            raise Exception("ivalid heading format")

    if block_type == block_type_code:
        if not (block.startswith("```") and block.endswith("```")):
            raise Exception("invalid code block format")

        children = list(
            map(lambda x: x.text_node_to_html_node(), text_to_textnodes(block[3:-3]))
        )

        return ParentNode(
            tag="pre", children=[ParentNode(tag="code", children=children)]
        )

    if block_type == block_type_quote:
        text = []
        for line in block.split("\n"):
            if not line.startswith(">"):
                raise Exception("invalid quote block format")

            text.append(line[1:])

        children = list(
            map(
                lambda x: x.text_node_to_html_node(), text_to_textnodes("\n".join(text))
            )
        )

        return ParentNode(tag="blockquote", children=children)

    if block_type == block_type_ordered_list:
        for index, line in enumerate(block.split("\n")):
            if not line.startswith(f"{index+1}. "):
                raise Exception("invalid ordered list format")

            html_nodes = list(
                map(lambda x: x.text_node_to_html_node(), text_to_textnodes(line[3:]))
            )
            children.append(ParentNode(tag="li", children=html_nodes))

        return ParentNode(tag="ol", children=children)

    if block_type == block_type_unordered_list:
        for index, line in enumerate(block.split("\n")):
            if not (line.startswith("* ") or line.startswith("- ")):
                raise Exception("invalid unordered list format")

            html_nodes = list(
                map(lambda x: x.text_node_to_html_node(), text_to_textnodes(line[2:]))
            )
            children.append(ParentNode(tag="li", children=html_nodes))

        return ParentNode(tag="ul", children=children)

    if block_type == block_type_paragraph:
        children = list(
            map(lambda x: x.text_node_to_html_node(), text_to_textnodes(block))
        )

        return ParentNode(tag="p", children=children)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    children = []

    for block in blocks:
        children.append(block_to_htmlnode(block, block_to_block_type(block)))

    return ParentNode(tag="div", children=children)
