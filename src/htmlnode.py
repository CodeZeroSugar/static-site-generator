class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html is not implemented for HTMLNode")

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
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode requires a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode requires a tag")
        if self.children is None:
            raise ValueError("ParentNode cannot have no children")
        if self.children == []:
            raise ValueError("ParentNode cannot have empty list for children")

        html_concat_child = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_concat_child = html_concat_child + child.to_html()

        html_concat_child = html_concat_child + f"</{self.tag}>"

        return html_concat_child
