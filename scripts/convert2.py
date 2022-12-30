import markdown
import jinja2
import os
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

POSTS_DIR = ROOT / "posts"
TEMPLATE_DIR = ROOT / "templates"
PAGE_TEMPLATE_FILE = "page.html"

BASE_URL = os.environ.get("DOMAIN", "http://0.0.0.0:5000/")

def no_p_markdown(non_p_string) -> str:
    ''' Strip enclosing paragraph marks, <p> ... </p>, 
        which markdown() forces, and which interfere with some jsnja2 layout
    '''
    non_p_string = re.subn("<p><a", "<a",non_p_string, 
                   flags=re.IGNORECASE)[0]
    non_p_string = re.subn("<\/a><\/p>", "</a>", non_p_string, 
                   flags=re.IGNORECASE)[0]
    return non_p_string

def generate():
    posts = POSTS_DIR.glob("*.md")
    extensions = ["extra", "smarty", "meta", "footnotes"]
    loader = jinja2.FileSystemLoader(searchpath=TEMPLATE_DIR)
    env = jinja2.Environment(loader=loader, autoescape=True)

    for post in posts:
        print(f"rendering {post}")
        
        url = f"{post.stem}.html"
        target_file = ROOT / url
        
        _md = markdown.Markdown(extensions=extensions, output_format="html5")
        
        content = post.read_text()

        html = _md.convert(content)


        doc = env.get_template(PAGE_TEMPLATE_FILE).render(
            content=html,
            baseurl=BASE_URL,
            url=url
        )

        # Writing the post html
        doc = no_p_markdown(doc)
        target_file.write_text(doc)
        
        
if __name__ == "__main__":
    pass
