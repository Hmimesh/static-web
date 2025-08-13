from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        else:
            return False
    
    def props_to_html(self):
        if self.props != None:
            result = ""

            for key, value in self.props.items():
                result += f' {key}="{value}"'
            return result
        
        else:
            return ""
    
    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'
    





class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props, children=None)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have value")
        
        result = ""

        prop = self.props_to_html()

        if self.tag == None:
            return self.value
        
        else:
            result += f'<{self.tag}{prop}>{self.value}</{self.tag}>'
            
        return result

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, props=props, children=children)

    def to_html(self):
        if self.tag == None:
            raise ValueError("all parent nodes must have tag")
        
        if self.children == None:
            raise ValueError("all parent nodes must have children")
        
        result = ""
        prop = self.props_to_html()
        result += f'<{self.tag}{prop}>'
        for child in self.children:
            result += child.to_html()
        result += f'</{self.tag}>'
        return result

def text_node_to_html_node(text_node):
    
    if text_node.text_type not in TextType:
        raise Exception("Not a valid Text Type")
    
    tag = None
    value = text_node.text
    url = None

    if text_node.text_type == TextType.NORMAL_TEXT:
        return LeafNode(tag=None, value=value)
    
    if text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=value)
    
    if text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=value)
    
    if text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=value)
    
    if text_node.text_type == TextType.LINKS:
        url = text_node.url
        return LeafNode(tag="a", value=value, props={'href': url})
    
    if text_node.text_type == TextType.IMAGES:
        url = text_node.url
        return LeafNode(tag='img',value="",props={"src": url, "alt": value})
