import unittest
from htmlnode import *
from textnode import *

class TestHTMLNode(unittest.TestCase):

	def test_init_default(self):
		# Test default implementation
		node = HTMLnode()
		self.assertIsNone(node.tag,
			msg="Test default implementation, tag")
		self.assertIsNone(node.value,
			msg="Test default implementation, value")
		self.assertIsNone(node.children,
			msg="Test default implementation, children")
		self.assertEqual(node.props, {},
			msg="Test default implementation, props")

	def test_init_with_values(self):
		# Test implementation with values
		node = HTMLnode("div", "content", ["child1", "child2"], {"class": "test"})
		self.assertEqual(node.tag, "div",
			msg="Test implementation with values, tag")
		self.assertEqual(node.value, "content",
			msg="Test implementation with values, value")
		self.assertEqual(node.children, ["child1", "child2"],
			msg="Test implementation with values, children")
		self.assertEqual(node.props, {"class": "test"},
			msg="Test implementation with values, props")

	def test_to_html_not_implemented(self):
		# Test feature not implemented
		node = HTMLnode()
		with self.assertRaises(NotImplementedError):
			node.to_html()

	def test_props_to_html_empty(self):
		# Test no props_to_html when no value
		node = HTMLnode()
		self.assertEqual(node.props_to_html(), "",
			msg="Test no props_to_html when no value")

	def test_props_to_html_single_prop(self):
		# Test no props_to_html when value
		node = HTMLnode(props={"class": "test"})
		self.assertEqual(node.props_to_html(), 'class="test"',
			msg="Test no props_to_html when value")

	def test_props_to_html_multiple_props(self):
		# Test no props_to_html when multiple value
		node = HTMLnode(props={"class": "test", "id": "main"})
		result = node.props_to_html()
		self.assertTrue(result == 'class="test" id="main"' or result == 'id="main" class="test"',
			msg="Test no props_to_html when multiple value")

	def test_repr_empty(self):
		# Test __repr__ returned correctly, no values
		node = HTMLnode()
		self.assertEqual(repr(node), "HTMLnode(tag=None, value=None, children=None, props=)",
			msg="Test __repr__ returned correctly, no values")

	def test_repr_with_values(self):
		# Test __repr__ returned correctly, with values
		node = HTMLnode("div", "content", ["child1", "child2"], {"class": "test"})
		expected = 'HTMLnode(tag=div, value=content, children=[\'child1\', \'child2\'], props=class="test")'
		self.assertEqual(repr(node), expected,
			msg="Test __repr__ returned correctly, with values")

	def test_props_none(self):
		# Test props explicit None value gives empty dict
		node = HTMLnode(props=None)
		self.assertEqual(node.props, {},
			msg="Test props explicit None value gives empty dict")

	def test_props_empty_dict(self):
		# Test props explicit None value gives empty dict
		node = HTMLnode(props={})
		self.assertEqual(node.props, {},
			msg="Test props explicit explicit None value gives empty dict")
	
class TestLeafNode(unittest.TestCase):
	def test_regular_node(self):
		# Test a regular node with tag and value
		node = LeafNode(tag="p", value="Hello World")
		self.assertEqual(node.to_html(), "<p>Hello World</p>", 
			msg="Test regular node HTML generation")

	def test_void_element(self):
		# Test void element (self-closing tag)
		node = LeafNode(tag="br")
		self.assertEqual(node.to_html(), "<br>", 
			msg="Test void element HTML generation")

	def test_void_element_with_props(self):
		# Test void element with properties
		node = LeafNode(tag="img", props={"src": "image.jpg", "alt": "test"})
		self.assertEqual(node.to_html(), '<img src="image.jpg" alt="test">', 
			msg="Test void element with props HTML generation")

	def test_text_only(self):
		# Test node with only text (no tag)
		node = LeafNode(value="Just text")
		self.assertEqual(node.to_html(), "Just text", 
			msg="Test text-only node HTML generation")

	def test_node_with_props(self):
		# Test regular node with properties
		node = LeafNode(tag="a", value="Click me", props={"href": "https://example.com"})
		self.assertEqual(node.to_html(), '<a href="https://example.com">Click me</a>', 
			msg="Test node with props HTML generation")

	def test_value_none_non_void(self):
		# Test ValueError raised when value is None for non-void element
		with self.assertRaises(ValueError, msg="Test ValueError for None value in non-void element"):
			node = LeafNode(tag="p")
			node.to_html()

	def test_value_none_void(self):
		# Test that void elements accept None value
		node = LeafNode(tag="hr")
		self.assertEqual(node.to_html(), "<hr>", 
			msg="Test void element accepts None value")

	def test_props_empty(self):
		# Test node with empty props
		node = LeafNode(tag="p", value="Text", props={})
		self.assertEqual(node.to_html(), "<p>Text</p>", 
			msg="Test node with empty props")

	def test_multiple_props(self):
		# Test node with multiple properties
		node = LeafNode(tag="div", value="Content", 
					   props={"class": "container", "id": "main", "data-test": "true"})
		self.assertEqual(node.to_html(), 
						'<div class="container" id="main" data-test="true">Content</div>', 
			msg="Test node with multiple props")

	def test_repr(self):
		# Test string representation
		node = LeafNode(tag="p", value="Text", props={"class": "test"})
		self.assertEqual(repr(node), 'LeafNode(tag=p, value=Text, props=class="test")', 
			msg="Test __repr__ output")

	def test_props_to_html(self):
		# Test props_to_html method
		node = LeafNode(tag="div", value="test", props={"class": "bold", "id": "main"})
		self.assertTrue(
			node.props_to_html() in ['class="bold" id="main"', 'id="main" class="bold"'],
			msg="Test props_to_html output"
		)

class TestParentNode(unittest.TestCase):
    def test_parent_node_basic(self):
		# ParentNode.to_html() and two LeafNode children
        child1 = LeafNode("p", "Paragraph 1")
        child2 = LeafNode("p", "Paragraph 2")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), "<div><p>Paragraph 1</p><p>Paragraph 2</p></div>",
			msg="ParentNode.to_html() and two LeafNode children")

    def test_parent_node_with_props(self):
		# ParentNode.to_html() and one LeafNode child
        child = LeafNode("p", "Content")
        parent = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"><p>Content</p></div>',
			msg="ParentNode.to_html() and one LeafNode child")

    def test_parent_node_nested(self):
		# ParentNode.to_html() with one ParentNode child with two LeafNode children
        leaf1 = LeafNode("p", "Paragraph 1")
        leaf2 = LeafNode("p", "Paragraph 2")
        inner_parent = ParentNode("div", [leaf1, leaf2], {"class": "inner"})
        outer_parent = ParentNode("div", [inner_parent], {"class": "outer"})
        expected = '<div class="outer"><div class="inner"><p>Paragraph 1</p><p>Paragraph 2</p></div></div>'
        self.assertEqual(outer_parent.to_html(), expected,
			msg="ParentNode.to_html() with one ParentNode child with two LeafNode children")

    def test_parent_node_invalid_no_tag(self):
		# ParentNode no tag ValueError
        with self.assertRaises(ValueError, msg="ParentNode no tag ValueError"):
            ParentNode(children=[LeafNode("p", "Content")]).to_html()

    def test_parent_node_invalid_no_children(self):
		# ParentNode no children ValueError
        with self.assertRaises(ValueError, msg="ParentNode no children ValueError"):
            ParentNode("div").to_html()

    def test_parent_node_invalid_with_value(self):
		# ParentNode forced value assignment, TypeError
        with self.assertRaises(TypeError, msg="ParentNode forced value assignment, TypeError"):
            ParentNode("div", [], value="This should raise an error")

    def test_parent_node_repr(self):
		# ParentNode and one LeafNodes child __repr__
        child = LeafNode("p", "Content")
        parent = ParentNode("div", [child], {"class": "container"})
        expected = 'ParentNode(tag=div, children=[LeafNode(tag=p, value=Content, props=)], props=class="container")'
        self.assertEqual(repr(parent), expected,
			msg="ParentNode.to_html() and two LeafNode children")

class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_plain_text(self):
        text_node = TextNode("Hello, world!", "text")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Hello, world!")

    def test_bold_text(self):
        text_node = TextNode("Bold text", "bold")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic_text(self):
        text_node = TextNode("Italic text", "italic")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")  # Note: This might be a bug in the original function
        self.assertEqual(html_node.value, "Italic text")

    def test_code_text(self):
        text_node = TextNode("print('Hello')", "code")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")

    def test_link(self):
        text_node = TextNode("Click here", "link", "https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        text_node = TextNode("", "image", "Alt text](https://example.com/image.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "Alt text"})

    def test_invalid_type(self):
        text_node = TextNode("Invalid", "invalid_type")
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(text_node)
        self.assertTrue("Incompatible text_type" in str(context.exception))

    def test_invalid_input(self):
        with self.assertRaises(Exception) as context:
            text_node_to_html_node("Not a TextNode")
        self.assertTrue("only accepts objects of the TextNode class" in str(context.exception))


if __name__ == '__main__':
	unittest.main()