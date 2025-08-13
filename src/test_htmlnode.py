import unittest

from textnode import *
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("<a>", None, None, {"href": "https://www.google.com", "target": "_blank"})
        check = node.props_to_html()
        self.assertEqual(check, ' href="https://www.google.com" target="_blank"')

        node2 = HTMLNode("<a>", None, None, {})
        self.assertEqual(node2.props_to_html(), "")

    def test_raise(self):
        node = HTMLNode("<a>", None, None, {"href": "https://www.google.com", "target": "_blank"})
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_eq(self):
        node = HTMLNode("<a>", None, None, {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("<a>", None, None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), node2.props_to_html())
        
        node3 = HTMLNode("<a>", "hey", "What", None)
        node4 = HTMLNode("<a>", "hey", "What", None)
        self.assertEqual(node3, node4)

    def test_not_eq(self):
        node = HTMLNode("<a>", None, "What", {"href": "https://www.google.com", "target": "_blank"})
        node2= HTMLNode("<a>", None, None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node, node2)

        node3 = HTMLNode("<a>", "hey", "What", None)
        node4 = HTMLNode("<a>", None, "What", None)
        self.assertNotEqual(node3, node4)
    

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello World")
        self.assertEqual(node.to_html(), "<p>Hello World</p>")
    
    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Hello world", {"href": "https://www.hellow.world"})
        self.assertEqual(node.to_html(), '<a href="https://www.hellow.world">Hello world</a>')

        node2 = LeafNode("a", "Hello world", {"href": "https://www.hellow.world", "target": "_blank"})
        self.assertEqual(node2.to_html(), '<a href="https://www.hellow.world" target="_blank">Hello world</a>')

    def test_leaf_no_tags(self):
        node = LeafNode(None, "hello world")
        self.assertEqual(node.to_html(), "hello world")
    
    def test_raising_errors(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )
    
    def test_to_html_with_recursion_children(self):
        child_node = LeafNode("a", "child", {"href": "https:www.google.com"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><a href="https:www.google.com">child</a></div>'
        )

    def test_text_node_to_html(self):
        node = TextNode("this is a text node", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "this is a text node")
    
    def test_bold(self):
        node = TextNode("this is a BOLD node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "this is a BOLD node")
    
    def test_italic(self):
        node = TextNode("this is a ItAlIc node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "this is a ItAlIc node")

    def test_code(self):
        node = TextNode("this is a `code` node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "this is a `code` node")
    
    def test_link(self):
        node = TextNode("this is a link node", TextType.LINKS, 'https://www.google.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "this is a link node")
        self.assertEqual(html_node.props,{'href': 'https://www.google.com'} )

    def test_images(self):
        node = TextNode("this is an image node", TextType.IMAGES, 'encrypt.pizza')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'encrypt.pizza', 'alt': 'this is an image node'})