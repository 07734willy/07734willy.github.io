from pygments.formatters import HtmlFormatter
from bs4 import BeautifulSoup
import markdown

from itertools import starmap
from shutil import copyfile
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

TEMPLATE_DIR = "templates"
BUILD_DIR = "docs"
ARTICLE_DIR = "articles"

def convert_markdown(text):
	extensions = [TexExtension(), 'codehilite', 'abbr', 'footnotes', 'tables', 'sane_lists']
	html = markdown.markdown(text, extensions=extensions)
	return html

def build_css(style):
	css = HtmlFormatter(style=style).get_style_defs()
	filepath = os.path.join(BUILD_DIR, "code.css")
	with open(filepath, "w") as f:
		f.write(css)

	src_filepath = os.path.join(TEMPLATE_DIR, "page.css")
	dst_filepath = os.path.join(BUILD_DIR, "page.css")
	copyfile(src_filepath, dst_filepath)

def make_page(markdown):
	content = convert_markdown(markdown)

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
	filepath = os.path.join(BUILD_DIR, filename)
	with open(filepath, "w") as f:
		f.write(str(data))

def build_about():
	filepath = os.path.join(TEMPLATE_DIR, "about.md")
	with open(filepath, "r") as f:
		markdown = f.read()
	
	soup = make_page(markdown)
	write_page("about.html", soup)

def build_index():
	src_filepath = os.path.join(BUILD_DIR, "about.html")
	dst_filepath = os.path.join(BUILD_DIR, "index.html")
	copyfile(src_filepath, dst_filepath)

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
	
	build_css(STYLE)
	build_index()

def main():
	build_site()

if __name__ == "__main__":
	main()
