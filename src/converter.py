from bs4 import BeautifulSoup
import markdown

import os

from style import MyStyle
from latextension import TexExtension

markdown.extension_configs = {
	'codehilite': {
		'guess_lang': False,
		'linenums': True,
	},
}

STYLE = CodeStyle

TEMPLATE_DIR = "templates"
ARTICLE_DIR = "articles"

def markdown_to_html(md_text):
	extensions = [TexExtension(), 'codehilite', 'abbr', 'footnotes', 'tables', 'sane_lists']
	html = markdown.markdown(md_text, extensions=extensions)
	return html

def markdown_to_soup(md_text):
	content = markdown_to_html(md_text)

	filepath = os.path.join(TEMPLATE_DIR, "page.html")
	with open(filepath, "r") as f:
		html = f.read()
	
	soup = BeautifulSoup(html, "html.parser")

	elem_content = soup.find(id="content-body")
	elem_content.append(BeautifulSoup(content, "html.parser"))

	return soup

def get_markdown_files():
	for root, dirnames, filenames in os.walk(ARTICLE_DIR):
		for filename in filenames:
			filepath = os.path.join(root, filename)
	
			yield filepath

