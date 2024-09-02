from constants import(
    block_type_code,
    block_type_heading,
    block_type_olist,
    block_type_paragraph,
    block_type_quote,
    block_type_ulist,
    
)

#A representation of a HTMLNode with the purpose of rendering itself in HTML
class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses must implement this method")

    def props_to_html(self):
        if self.props is None:
            return ""
        html_string = ""
        for key, value in self.props.items():
            html_string += f" {key}=\"{value}\""
        return html_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

#An HTMLNode with a single html tag and no children
class LeafNode(HTMLNode):
    def __init__(self,tag ,value,props = None): 
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: no value") 
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
# An HTML node that has children and handles the nesting of them.    
class ParentNode(HTMLNode):
    def __init__(self,tag,children,props = None):
        super().__init__(tag,None,children,props)

    def to_html(self):
        if  self.tag == None:
            raise ValueError("Invalid tag: Must have a tag")
        if self.children == None:
            raise ValueError("No children")

        html_string = ""
        for child in self.children: 
            html_string += child.to_html()
        return f"<{self.tag}>{html_string}</{self.tag}>"
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
