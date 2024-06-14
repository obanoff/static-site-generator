class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplemented("Subclasses should implement this method")

    def props_to_html(self):
        str = ""
        if self.props is not None:
            for key, value in self.props.items():
                str += f' {key}="{value}"'
                
        return str

    def __repr__(self) -> str:
        return f"HTMLNode\n{self.tag}\n{self.value}\n{self.children}\n{self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("value not provided")

        if not self.tag:
            return f"{self.value}"

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag not provided")

        if not self.children:
            raise ValueError("children not provided")

        children = ""
        for child in self.children:
            children += child.to_html()
            
        return f'<{self.tag}{self.props_to_html()}>{children}</{self.tag}>'

            










