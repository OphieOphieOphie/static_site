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
