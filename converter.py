from pygments.formatters import HtmlFormatter
from bs4 import BeautifulSoup
import markdown

from itertools import starmap
import os

from style import MyStyle
from latextension import TexExtension

markdown.extension_configs = {
	'codehilite': {
		'guess_lang': False,
		'linenums': True,
	},
}

STYLE = MyStyle
TEMPLATE_PAGE = "page.html"

def convert_markdown(text):
	extensions = [TexExtension(), 'codehilite', 'abbr', 'footnotes', 'tables', 'sane_lists']
	html = markdown.markdown(text, extensions=extensions)
	return html

def make_css(style):
	css = HtmlFormatter(style=style).get_style_defs()
	with open("docs/code.css", "w") as f:
		f.write(css)

def make_page(markdown):
	content = convert_markdown(markdown)

	with open(TEMPLATE_PAGE, "r") as f:
		html = f.read()
	
	soup = BeautifulSoup(html, "html.parser")

	elem_content = soup.find(id="content-body")
	elem_content.append(BeautifulSoup(content, "html.parser"))

	return soup

def get_markdown_files():
	for root, dirnames, filenames in os.walk("articles/"):
		for filename in filenames:
			filepath = os.path.join(root, filename)
	
			yield filepath

def get_article_title(soup):
	title = soup.find("h1").string
	return title

def build_sitemap(pages):
	header = "# Sitemap\n---\n"
	
	def to_link(title, filepage):
		return f"* [{title}]({filepage})"
		
	body = "\n".join(starmap(to_link, pages))

	markdown = header + body
	soup = make_page(markdown)

	write_page("sitemap.html", soup)
	
def write_page(filename, data):
	filepath = os.path.join("docs", filename)
	with open(filepath, "w") as f:
		f.write(str(data))

def build_about():
	with open("about.md", "r") as f:
		markdown = f.read()
	
	soup = make_page(markdown)
	write_page("about.html", soup)

def build_index():
	with open("docs/about.html", "r") as f:
		html = f.read()

	with open("docs/index.html", "w") as f:
		f.write(html)

def build_site():
	pages = []

	build_about()
	
	for filepath in get_markdown_files():
		with open(filepath, "r") as f:
			markdown = f.read()

		soup = make_page(markdown)
		filename = os.path.basename(filepath)
		filepage = os.path.splitext(filename)[0] + ".html"
		
		page = (get_article_title(soup), filepage)
		pages.append(page)

		write_page(filepage, soup)

	soup = build_sitemap(pages)
	
	make_css(STYLE)
	
	build_index()

def main():
	"""
	html = make_page("test.md")
	make_css(STYLE)
	print(html)
	"""
	build_site()

if __name__ == "__main__":
	main()
