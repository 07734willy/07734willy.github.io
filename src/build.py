from pygments.formatters import HtmlFormatter

from shutil import copyfile
from itertools import starmap
import os

from converter import TEMPLATE_DIR, markdown_to_soup, get_markdown_files
from style import CodeStyle

BUILD_DIR = "docs"
STYLE = CodeStyle

def get_article_title(soup):
	title = soup.find("h1").string
	return title

def write_page(filename, data):
	filepath = os.path.join(BUILD_DIR, filename)
	with open(filepath, "w") as f:
		f.write(str(data))

def build_css(style):
	css = HtmlFormatter(style=style).get_style_defs()
	filepath = os.path.join(BUILD_DIR, "code.css")
	with open(filepath, "w") as f:
		f.write(css)

	src_filepath = os.path.join(TEMPLATE_DIR, "page.css")
	dst_filepath = os.path.join(BUILD_DIR, "page.css")
	copyfile(src_filepath, dst_filepath)

def build_sitemap(pages):
	header = "# Sitemap\n---\n"
	
	def to_link(title, filepage):
		return f"* [{title}]({filepage})"
		
	body = "\n".join(starmap(to_link, pages))

	md_text = header + body
	soup = markdown_to_soup(md_text)

	write_page("sitemap.html", soup)

def build_about():
	filepath = os.path.join(TEMPLATE_DIR, "about.md")
	with open(filepath, "r") as f:
		md_text = f.read()
	
	soup = markdown_to_soup(md_text)
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
			md_text = f.read()

		soup = markdown_to_soup(md_text)
		filename = os.path.basename(filepath)
		filepage = os.path.splitext(filename)[0] + ".html"
		
		page = (get_article_title(soup), filepage)
		pages.append(page)

		write_page(filepage, soup)

	soup = build_sitemap(pages)
	
	build_css(STYLE)
	build_index()

if __name__ == "__main__":
	build_site()
