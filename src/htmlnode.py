class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        # If tag is None, prefer value, then children, else empty string
        if self.tag is None:
            if self.value is not None:
                return self.value

            if self.children is not None:
                children_html = ""
                for child in self.children:
                    children_html += child.to_html()
                return children_html

            return ""

        # tag is present — render with either children or value
        props_html = self.props_to_html()

        if self.children is not None:
            children_html = ""
            for child in self.children:
                children_html += child.to_html()
            return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"

        # no children
        value = self.value if self.value is not None else ""
        return f"<{self.tag}{props_html}>{value}</{self.tag}>"

    def props_to_html(self):

        if self.props is None:
            return ""

        result = ""

        for key, value in self.props.items():
            result += f' {key}="{value}"'

        return result
    
    def __repr__(self):
        return f"HTMLNODE(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"