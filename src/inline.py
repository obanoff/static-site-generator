import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

valid_delimiters = {
    "*": text_type_italic,
    "**": text_type_bold,
    "`": text_type_code,
}


def split_nodes_delimiter(old_notes, delimiter, text_type):
    if valid_delimiters[delimiter] != text_type:
        raise Exception("not valid delimiter")

    new_nodes = []

    for node in old_notes:
        open, close = -1, 0

        i = 0
        while i < len(node.text):
            if i + len(delimiter) <= len(node.text):
                if node.text[i : i + len(delimiter)] == delimiter:

                    # if no text within open and close delimiters (that can form another dilimeters as well) skip it
                    if (
                        node.text[i + len(delimiter) : i + len(delimiter) * 2]
                        == delimiter
                    ):
                        i += len(delimiter) * 2
                        continue

                    if open == -1 and node.text[close:i] != "":
                        new_nodes.append(TextNode(node.text[close:i], text_type_text))

                    if open != -1:
                        close = i + len(delimiter)
                        new_nodes.append(
                            TextNode(
                                node.text[
                                    open + len(delimiter) : close - len(delimiter)
                                ],
                                text_type,
                            )
                        )
                        open = -1
                    else:
                        open = i

            i += 1

        # open was not reset because close tag was not found
        if open != -1:
            raise Exception("invalid Markdown syntax")

        # append the leftover if exists
        if node.text[close:] != "":
            new_nodes.append(TextNode(node.text[close:], text_type_text))

    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"

    matches = re.findall(pattern, text)

    return matches


def extract_markdown_links(text):
    pattern = r"\[(.*?)]\((.*?)\)"

    matches = re.findall(pattern, text)

    return matches


def extract_nodes(text_type, nodes):
    new_nodes = []

    for node in nodes:
        if node.text_type != text_type_text:
            if node.text_type == text_type:
                new_nodes.append(node)
                continue
            else:
                raise Exception("not valid text_type")

        matches = (
            extract_markdown_images(node.text)
            if text_type == text_type_image
            else extract_markdown_links(node.text)
        )

        if len(matches) == 0:
            if node.text_type == text_type_text:
                new_nodes.append(TextNode(node.text, text_type_text))
            else:
                raise Exception(f"not valid Markdown syntax")

            continue

        parts = []

        for i in range(0, len(matches)):
            if i == 0:
                text = node.text
            else:
                text = parts[1]

            split_pattern = (
                f"![{matches[i][0]}]({matches[i][1]})"
                if text_type == text_type_image
                else f"[{matches[i][0]}]({matches[i][1]})"
            )
            parts = text.split(split_pattern, 1)

            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], text_type_text))

            # append delimiter (image or link)
            new_nodes.append(TextNode(matches[i][0], text_type, matches[i][1]))

            # if the last match - append a text leftover (after the delimiter) if any
            if i == len(matches) - 1 and parts[1] != "":
                new_nodes.append(TextNode(parts[1], text_type_text))

    return new_nodes


def split_nodes_image(old_nodes):
    return extract_nodes(text_type_image, old_nodes)


def split_nodes_link(old_nodes):
    return extract_nodes(text_type_link, old_nodes)


def text_to_textnodes(text):
    def extract_italic(text):
        return split_nodes_delimiter(
            [TextNode(text, text_type_text)], "*", text_type_italic
        )

    def extract_bold(old_nodes):
        return split_nodes_delimiter(old_nodes, "**", text_type_bold)

    def extract_code(old_nodes):
        return split_nodes_delimiter(old_nodes, "`", text_type_code)

    def filter(old_nodes, func):
        new_nodes = []
        for node in old_nodes:
            if node.text_type == text_type_text:
                new_nodes.extend(func([node]))
                continue

            new_nodes.append(node)

        return new_nodes

    nodes = filter(
        filter(
            filter(filter(extract_italic(text), extract_bold), extract_code),
            split_nodes_image,
        ),
        split_nodes_link,
    )

    return nodes
