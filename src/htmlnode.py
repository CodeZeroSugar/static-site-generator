class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""

        if not isinstance(self.props, dict):
            raise Exception("invalid input for HTMLNode props")

        html_attr = ""
        for key, value in self.props.items():
            to_add = f' {key}="{value}"'
            html_attr = html_attr + to_add

        return html_attr

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        if self.props is None:
            self.props = ""
        else:
            self.props = self.props_to_html()

        return f"<{self.tag}{self.props}>{self.value}</{self.tag}>"
