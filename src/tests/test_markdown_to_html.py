import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from markdown_to_blocks import markdown_to_html_node

class TestMarkdownToHtml(unittest.TestCase):
    def test_heading_paragraph(self):
        md = "# Hello\n\nThis is **bold** and _italic_."
        html = markdown_to_html_node(md).to_html()
        self.assertIn("<div>", html)
        self.assertIn("<h1>Hello</h1>", html)
        self.assertIn("<p>This is <b>bold</b> and <i>italic</i>.</p>", html)
        self.assertTrue(html.endswith("</div>"))

    def test_lists_and_code(self):
        md = "- One\n- Two\n\n1. First\n2. Second\n\n````\ncode `not inline`\n````"
        html = markdown_to_html_node(md).to_html()
        self.assertIn("<ul><li>One</li><li>Two</li></ul>", html)
        self.assertIn("<ol><li>First</li><li>Second</li></ol>", html)
        self.assertIn("<pre><code>code `not inline`</code></pre>", html)

if __name__ == "__main__":
    unittest.main()

