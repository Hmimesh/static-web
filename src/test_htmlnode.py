import unittest

from htmlnode import HTMLNode, LeafNode

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