import unittest
from textnode import TextNode
import htmlnode
from markdown_parser import *

class TestMarkdownParser(unittest.TestCase):

    def test_plain_text(self):
        text = "Hello, world!"
        result = raw_text_to_markdown(text)
        self.assertEqual(result, "<p>Hello, world!</p>")

    def test_bold(self):
        text = "Hello **bold** world"
        result = raw_text_to_markdown(text)
        self.assertEqual(result, "<p>Hello <b>bold</b> world</p>")

    def test_italic(self):
        text = "Hello *italic* world"
        result = raw_text_to_markdown(text)
        self.assertEqual(result, "<p>Hello <i>italic</i> world</p>")

    def test_code(self):
        text = "Here's some `inline code`"
        result = raw_text_to_markdown(text)
        self.assertEqual(result, "<p>Here's some <code>inline code</code></p>")

    def test_link(self):
        text = "Check out [this link](https://example.com)"
        result = raw_text_to_markdown(text)
        self.assertEqual(result, '<p>Check out <a href="https://example.com">this link</a></p>')

    def test_image(self):
        text = "An image: ![alt text](image.jpg)"
        result = raw_text_to_markdown(text)
        self.assertEqual(result, '<p>An image: <img src="image.jpg" alt="alt text"></p>')

    def test_multiple_elements(self):
        text = "**Bold** and *italic* and `code`"
        result = raw_text_to_markdown(text)
        self.assertEqual(result, "<p><b>Bold</b> and <i>italic</i> and <code>code</code></p>")

    def test_unclosed_markdown(self):
        text = "This is *unclosed"
        result = raw_text_to_markdown(text)
        self.assertEqual(result, "<p>This is *unclosed</p>")

    def test_escaped_markdown(self):
        text = "This is \*not markdown\* and this is \`not code\`"
        result = raw_text_to_markdown(text)
        self.assertEqual(result, "<p>This is *not markdown* and this is `not code`</p>")

    def test_escaped_multiple(self):
        text = "Escaped \* \** \` \["
        result = raw_text_to_markdown(text)
        self.assertEqual(result, "<p>Escaped * ** ` [</p>")

    def test_mixed_escaped_and_markdown(self):
        text = "**Bold** and \*not bold\* and *italic*"
        result = raw_text_to_markdown(text)
        self.assertEqual(result, "<p><b>Bold</b> and *not bold* and <i>italic</i></p>")

    def test_empty_string(self):
        text = ""
        result = raw_text_to_markdown(text)
        self.assertEqual(result, "<p></p>")

    def test_multiple_paragraphs(self):
        text = "First paragraph\n\nSecond paragraph"
        result = raw_text_to_markdown(text)
        self.assertEqual(result, "<p>First paragraph\n\nSecond paragraph</p>")

    def test_complex_mixed_content(self):
        text = "Here's **bold** and *italic* text with a [link](https://example.com) and `code`.\n\n![Image](image.jpg)\n\nEscaped \\* \\` \\["
        result = raw_text_to_markdown(text)
        expected = "<p>Here's <b>bold</b> and <i>italic</i> text with a <a href=\"https://example.com\">link</a> and <code>code</code>.\n\n<img src=\"image.jpg\" alt=\"Image\">\n\nEscaped * ` [</p>"
        self.assertEqual(result, expected)

    def test_backslash_at_end(self):
        text = "This ends with a backslash\\"
        result = raw_text_to_markdown(text)
        self.assertEqual(result, "<p>This ends with a backslash\\</p>")

if __name__ == '__main__':
    unittest.main()