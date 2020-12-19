from markdown.extensions.codehilite import HiliteTreeprocessor as HTP
from markdown.treeprocessors import Treeprocessor
from markdown.inlinepatterns import InlineProcessor
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from latex2mathml.converter import convert as convert_latex
import xml.etree.ElementTree as etree


import re

def tex_to_mathml(data):
	tex = HTP.code_unescape(None, data)
	html = convert_latex(tex).strip()
	return html

def wrap_inline_math(data):
	math_html = tex_to_mathml(data)
	html = f"<span class=\"inline-math\">{math_html}</span>"
	return html

def wrap_block_math(data):
	math_html = tex_to_mathml(data)
	html = f"<div class=\"block-math\">{math_html}</div>"
	return html

class TexTreeprocessor(Treeprocessor):
		
	def run(self, root):
		blocks = root.iter('pre')
		for block in blocks:
			if len(block) == 1 and block[0].tag == 'code':
				code = block[0].text
				if not code.startswith(":::latex"):
					continue

				regex = r"(?:^|(?<=\n)):::latex\s*"

				html = "<br>".join(map(wrap_block_math, re.split(regex, code)[1:]))
				placeholder = self.md.htmlStash.store(html)
				
				block.clear()
				block.tag = 'p'
				block.text = placeholder
	

class TexBlockProcessor(BlockProcessor):
	PATTERN = r"^([\s\S]*?)(?<![\w\$])(\$(?!\s)((?:[^\$]|\\\$)+?)(?<!\s)\$)(?![\w\$])([\s\S]*)$"

	def __init__(self, md):
		self.md = md
		super().__init__(md.parser)

	def test(self, parent, block):
		return re.match(self.PATTERN, block)

	def run(self, parent, blocks):
		self.add_tex_seg(parent, blocks[0])
		del blocks[0]
		return True

	def add_span(self, parent, text):
		e = etree.SubElement(parent, 'span')
		e.text = text

	def add_tex_seg(self, parent, block):
		if not block:
			return

		if not re.match(self.PATTERN, block):
			self.add_span(parent, block)
			return

		match = re.match(self.PATTERN, block)
		
		if match.group(1):
			self.add_span(parent, match.group(1))

		html = wrap_inline_math(match.group(3))
		placeholder = self.md.htmlStash.store(html)
		self.add_span(parent, placeholder)

		self.add_tex_seg(parent, match.group(4))
	
class TexExtension(Extension):

	def extendMarkdown(self, md):
		treeprocessor = TexTreeprocessor(md)
		blockprocessor = TexBlockProcessor(md)
		md.treeprocessors.register(treeprocessor, 'textree', 31)
		md.parser.blockprocessors.register(blockprocessor, 'texblock', 18)

		md.registerExtension(self)
