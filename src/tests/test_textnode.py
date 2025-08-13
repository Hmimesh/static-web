import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("this is an image text", TextType.IMAGES, "https://upload.wikimedia.org/wikipedia/commons/8/88/Danny_DeVito_cropped_and_edited_for_brightness.jpg")
        node4 = TextNode("this is an image text", TextType.IMAGES, "https://upload.wikimedia.org/wikipedia/commons/8/88/Danny_DeVito_cropped_and_edited_for_brightness.jpg")
        self.assertEqual(node3, node4)

    def test_not_eq(self):
        node_2 = TextNode("This is a link node", TextType.LINKS, "https://www.google.com/search?client=firefox-b-d&q=Danny+devito")
        node_3 = TextNode("This is a BOLD text", TextType.BOLD)
        self.assertNotEqual(node_2, node_3)

        node_4 =TextNode("this is an image text", TextType.IMAGES, "https://upload.wikimedia.org/wikipedia/commons/8/88/Danny_DeVito_cropped_and_edited_for_brightness.jpg")
        self.assertNotEqual(node_2, node_4)

    def test_node_type_not_eq(self):
        node = TextNode("this is an image text", TextType.IMAGES, "https://upload.wikimedia.org/wikipedia/commons/8/88/Danny_DeVito_cropped_and_edited_for_brightness.jpg")
        node2 = TextNode("this is an image text", TextType.LINKS, "https://upload.wikimedia.org/wikipedia/commons/8/88/Danny_DeVito_cropped_and_edited_for_brightness.jpg")
        self.assertNotEqual(node, node2)


        
if __name__ == "__main__":
    unittest.main()