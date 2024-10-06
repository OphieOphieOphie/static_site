import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", "bold")
		node2 = TextNode("This is a text node", "bold")
		self.assertEqual(node, node2)

	def test_self_identity(self):
		node = TextNode("Self node", "edon fleS")
		self.assertIs(node, node)

	def test_not_eq(self):
		node = TextNode("1","2")
		node2 = TextNode("2","2")
		self.assertNotEqual(node, node2)

	def test_nil_url(self):
		node = TextNode("1","2")
		self.assertTrue(node.url is None)

if __name__ == "__main__":
	unittest.main()
