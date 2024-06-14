import re
from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

valid_delimiters = {
    "*": text_type_italic,
    "**": text_type_bold,
    "`": text_type_code,
}


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def text_node_to_html_node(self):
        if self.text_type == text_type_text:
            return LeafNode(None, self.text)

        if self.text_type == text_type_bold:
            return LeafNode("b", self.text)

        if self.text_type == text_type_italic:
            return LeafNode("i", self.text)

        if self.text_type == text_type_code:
            return LeafNode("code", self.text)

        if self.text_type == text_type_link:
            return LeafNode("a", self.text, {"href": self.url})

        if self.text_type == text_type_image:
            return LeafNode("img", "", {"src": self.url, "alt": self.text})

        raise Exception("invalid text type")


        

def split_nodes_delimiter(old_notes, delimiter, text_type):
    if valid_delimiters[delimiter] != text_type:
        raise Exception("not valid delimiter")

    new_nodes = []

    for node in old_notes:
        open, close = -1, 0

        i = 0
        while i < len(node.text):
            if i + len(delimiter) <= len(node.text):
                if node.text[i:i+len(delimiter)] == delimiter:

                    # if no text within open and close delimiters (that can form another dilimeters as well) skip it 
                    if node.text[i+len(delimiter):i+len(delimiter)*2] == delimiter: 
                        i += len(delimiter)*2
                        continue

                    if open == -1 and node.text[close:i] != "":
                        new_nodes.append(TextNode(node.text[close:i], text_type_text))

                    if open != -1:
                        close = i + len(delimiter)
                        new_nodes.append(TextNode(node.text[open:close], text_type))
                        open = -1
                    else:
                        open = i

            i += 1

        # open was not reset because close tag was not found
        if open != -1: raise Exception("invalid Markdown syntax")

        # append the leftover if exists
        if node.text[close:] != "": new_nodes.append(TextNode(node.text[close:], text_type_text))

    return new_nodes



def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"

    matches = re.findall(pattern, text)

    return matches


def extract_markdown_links(text):
    pattern = r"\[(.*?)]\((.*?)\)"

    matches = re.findall(pattern, text)

    return matches
        
