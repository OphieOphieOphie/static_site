import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
	def test_all_none(self):
		# Test default values of None
		node = HTMLnode()
		self.assertTrue(node.tag==node.value==node.children and node.props=={}, msg = "Test default values of None")

	def test_props(self):
		# Test props with multiple values
		node = HTMLnode(props={"a":"b","c":"d"})
		self.assertEqual(node.props_to_html(), 'a="b" c="d"', msg = "Test props with multiple values")

	def test_props_empty(self):
		# Test when props is None or an empty dictionary
		node = HTMLnode(tag="p", value=None, children=None, props={})
		self.assertEqual(node.props_to_html(), "", msg = "Test when props is None or an empty dictionary")

	def test_tag_and_value(self):
	   	# Test if the tag and value are correctly set
		node = HTMLnode(tag="h1", value="Hello World", children=None, props=None)
		self.assertEqual(node.tag, "h1")
		self.assertEqual(node.value, "Hello World", msg = "Test if the tag and value are correctly set")

	def test_children(self):
		# Test if children are correctly initialized
		child_node = HTMLnode(tag="span", value="Child", children=None, props=None)
		parent_node = HTMLnode(tag="div", value="Parent", children=[child_node], props=None)
		self.assertEqual(parent_node.children, [child_node], msg = "Test if children are correctly initialized")

	def test_repr(self):
		# Test __repr__ output for a node with props
		node = HTMLnode(tag="p", value="Text", children=None, props={"a": "b"})
		self.assertEqual(repr(node), 'HTMLnode(tag=p, value=Text, children=None, props=a="b")', msg = "Test __repr__ output for a node with props")
	
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

if __name__ == '__main__':
	unittest.main()