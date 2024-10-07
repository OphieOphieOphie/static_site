from textnode import TextNode

class HTMLnode:
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props or {}

	def to_html(self):
		raise NotImplementedError("to be implemented")

	def props_to_html(self):
		if not self.props: 
			return ""
		return " ".join(f'{i}="{v}"' for i, v in self.props.items())

	def __repr__(self):
		return f"HTMLnode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props_to_html()})"

class LeafNode(HTMLnode):

	VOID_ELEMENTS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input','link', 'meta', 'source', 'track', 'wbr'}

	def __init__(self, tag=None, value=None, props=None):
		super().__init__(tag, value, None, props)

	def to_html(self):
	
		if self.tag not in self.VOID_ELEMENTS and self.value is None:
			raise ValueError("Value is required and cannot be None for non-void elements")		
		
		props_str = self.props_to_html()
		
		if self.tag in self.VOID_ELEMENTS:
			return f"<{self.tag}{' ' + props_str if props_str else ''}>"

		if self.tag is None:
			return str(self.value)

		return f"<{self.tag}{' ' + props_str if props_str else ''}>{self.value}</{self.tag}>"
	
	def __repr__(self):
		props_str = self.props_to_html() if self.props else ""
		return f"LeafNode(tag={self.tag}, value={self.value}, props={props_str})"

class ParentNode(HTMLnode):

	def __init__(self, tag=None, children=None, props=None):
		super().__init__(tag, None, children, props)

	def to_html(self):
	
		if self.tag is None:
			raise ValueError("Value for ParentNode.tag is required and cannot be None")		
		
		if self.children is None:
			raise ValueError("Value for ParentNode.children is required and cannot be None")

		props_str = self.props_to_html()

		contents = "".join(i.to_html() for i in self.children)

		return f"<{self.tag}{' ' + props_str if props_str else ''}>{contents}</{self.tag}>"
	
	def __repr__(self):
		props_str = self.props_to_html() if self.props else ""
		return f"ParentNode(tag={self.tag}, children={self.children}, props={props_str})"

def text_node_to_html_node(text_node):
	if not isinstance(text_node, TextNode): 
		raise Exception("text_node_to_html_node only accepts objects of the TextNode class")

	text, text_type, url, alt = text_node.text, text_node.text_type, text_node.url, ""
	if text_type not in ("text","bold","italic","code","link","image"): raise Exception(f"Incompatible text_type: {text_type}")

	if url and text_type == "image":
		alt_ind = url.index("](")
		alt, url = url[:alt_ind], url[alt_ind+2:]

	return {"text":LeafNode(value=text),
		 "bold":LeafNode("b",text),
		 "italic":LeafNode("i",text),
		 "code":LeafNode("code",text),
		 "link":LeafNode("a",text,{"href":url}),
		 "image":LeafNode("img","",{"src":url,"alt":alt})}.get(text_type)