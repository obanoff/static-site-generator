from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


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

    def __hash__(self):
        return hash((self.text, self.text_type, self.url))

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
