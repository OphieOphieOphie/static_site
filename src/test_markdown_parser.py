import unittest
from markdown_parser import *

class TestNestedMarkdownParser(unittest.TestCase):

    def test_plain_text(self):
        self.assertEqual(raw_text_to_markdown("Hello, world!"), "Hello, world!")

    def test_bold(self):
        self.assertEqual(raw_text_to_markdown("**Bold text**"), "<b>Bold text</b>")

    def test_italic(self):
        self.assertEqual(raw_text_to_markdown("*Italic text*"), "<i>Italic text</i>")

    def test_bold_italic(self):
        self.assertEqual(raw_text_to_markdown("***Bold and italic***"), "<i><b>Bold and italic</b></i>")

    def test_nested_bold_italic(self):
        self.assertEqual(raw_text_to_markdown("**Bold with *italic* inside**"), "<b>Bold with <i>italic</i> inside</b>")

    def test_italic_bold(self):
        self.assertEqual(raw_text_to_markdown("*Italic with **bold** inside*"), "<i>Italic with <b>bold</b> inside</i>")

    def test_code(self):
        self.assertEqual(raw_text_to_markdown("`Code text`"), "<code>Code text</code>")

    def test_link(self):
        self.assertEqual(raw_text_to_markdown("[Link text](https://example.com)"), '<a href="https://example.com">Link text</a>')

    def test_image(self):
        self.assertEqual(raw_text_to_markdown("![Alt text](image.jpg)"), '<img src="image.jpg" alt="Alt text">')

    def test_complex_nesting(self):
        input_text = "**Bold *with italic* and `code` and [link](https://example.com)**"
        expected_output = '<b>Bold <i>with italic</i> and <code>code</code> and <a href="https://example.com">link</a></b>'
        self.assertEqual(raw_text_to_markdown(input_text), expected_output)

    def test_multiple_paragraphs(self):
        input_text = "First paragraph\n\nSecond paragraph"
        expected_output = "First paragraph\n\nSecond paragraph"
        self.assertEqual(raw_text_to_markdown(input_text), expected_output)

    ### more escaped tests

    def test_unclosed_bold(self):
        with self.assertRaises(Exception):
            raw_text_to_markdown("**Unclosed bold")

    def test_unclosed_italic(self):
        with self.assertRaises(Exception):
            raw_text_to_markdown("*Unclosed italic")

    def test_invalid_nesting(self):
        with self.assertRaises(Exception):
            raw_text_to_markdown("*Italic [with unclosed](http://example.com link*")

    def test_escaped_characters(self):
        self.assertEqual(raw_text_to_markdown("\\*Not italic\\*"), "*Not italic*")

    def test_bold_italic_combinations(self):
        self.assertEqual(raw_text_to_markdown("***Bold italic*** and **bold** and *italic*"), 
                         "<i><b>Bold italic</b></i> and <b>bold</b> and <i>italic</i>")

    def test_escaped_asterisk(self):
        self.assertEqual(raw_text_to_markdown("This is not \\*italic\\*"), "This is not *italic*")

    def test_escaped_double_asterisk(self):
        self.assertEqual(raw_text_to_markdown("This is not \\*\\*bold\\*\\*"), "This is not **bold**")

    def test_escaped_backtick(self):
        self.assertEqual(raw_text_to_markdown("This is not \\`code\\`"), "This is not `code`")

    def test_escaped_square_bracket(self):
        self.assertEqual(raw_text_to_markdown("This is not \\[a link\\]"), "This is not [a link\\]")

    def test_escaped_parenthesis(self):
        self.assertEqual(raw_text_to_markdown("This is not a \\(link\\)"), "This is not a \\(link\\)")

    def test_escaped_exclamation(self):
        self.assertEqual(raw_text_to_markdown("This is not an \\!\\[image\\]"), "This is not an ![image\\]")

    def test_escaped_backslash(self):
        self.assertEqual(raw_text_to_markdown("This is a backslash: \\\\"), "This is a backslash: \\\\")

    def test_escaped_in_bold(self):
        self.assertEqual(raw_text_to_markdown("**Bold with \\* inside**"), "<b>Bold with * inside</b>")

    def test_escaped_in_italic(self):
        self.assertEqual(raw_text_to_markdown("*Italic with \\** inside*"), "<i>Italic with ** inside</i>")

    def test_escaped_in_code(self):
        self.assertEqual(raw_text_to_markdown("`Code with \\` inside`"), "<code>Code with ` inside</code>")

    def test_escaped_in_link_text(self):
        self.assertEqual(raw_text_to_markdown("[Link with \\[brackets\\]](https://example.com)"), 
                         '<a href="https://example.com">Link with [brackets]</a>')

    def test_escaped_in_image_alt(self):
        self.assertEqual(raw_text_to_markdown("![Image with \\[brackets\\]](image.jpg)"), 
                         '<img src="image.jpg" alt="Image with [brackets]">')

    def test_multiple_escapes(self):
        self.assertEqual(raw_text_to_markdown("\\*\\*\\*Not bold or italic\\*\\*\\*"), "***Not bold or italic***")

    def test_escape_at_end_of_string(self):
        self.assertEqual(raw_text_to_markdown("This ends with a backslash\\"), "This ends with a backslash\\")

    def test_escape_before_space(self):
        self.assertEqual(raw_text_to_markdown("This has an escaped\\ space"), "This has an escaped\\ space")

    def test_multiple_escaped_sequences(self):
        input_text = "\\*italic\\* \\**bold\\** \\`code\\` \\[link](http://example.com)"
        expected_output = "*italic* **bold** `code` [link](http://example.com)"
        self.assertEqual(raw_text_to_markdown(input_text), expected_output)

    def test_multiple_escaped_sequences_slash_retained(self):
        input_text = "\\*italic\\* \\**bold\\** \\`code\\` \\[link\\](http://example.com)"
        expected_output = "*italic* **bold** `code` [link\\](http://example.com)"
        self.assertEqual(raw_text_to_markdown(input_text), expected_output)

    def test_link_nested_in_alt_text(self):
        input_text = "![Image [ ***this link*** ](https://example.com) \\[brackets\\]](image.jpg)"
        expected_output = '<img src="image.jpg" alt="Image <a href="https://example.com"> <i><b>this link</b></i> </a> [brackets]">'
        self.assertEqual(raw_text_to_markdown(input_text), expected_output)
    
    def test_image_nested_in_link_text(self):
        input_text = "[ ***this An image: ![alt text](image.jpg) link*** ](https://example.com)"
        expected_output = '<a href="https://example.com"> <i><b>this An image: <img src="image.jpg" alt="alt text"> link</b></i> </a>'
        self.assertEqual(raw_text_to_markdown(input_text), expected_output)

if __name__ == '__main__':
    unittest.main()