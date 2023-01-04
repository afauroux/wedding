import markdown
import jinja2
import os
import re
from datetime import datetime
from email.utils import formatdate, format_datetime  # for RFC2822 formatting
from pathlib import Path
import yaml

ROOT = Path(__file__).parent.parent

POSTS_DIR = ROOT / "posts"
TEMPLATE_DIR = ROOT / "templates"
PAGE_TEMPLATE_FILE = "page.html"

BASE_URL = os.environ.get("DOMAIN", "http://0.0.0.0:5000/")


def no_p_markdown(non_p_string) -> str:
    ''' Strip enclosing paragraph marks, <p> ... </p>, 
        which markdown() forces, and which interfere with some jsnja2 layout
    '''
    non_p_string = re.subn("<p><a", "<a", non_p_string,
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

        # retrieving the config infos
        config = yaml.load(Path("config.yaml").read_text(
            encoding="utf8"), Loader=yaml.FullLoader)
        config['updatedTime'] = str(datetime.now())

        url = f"{post.stem}.html"
        target_file = ROOT / url

        _md = markdown.Markdown(extensions=extensions, output_format="html5")

        content = post.read_text(encoding="utf8")

        html = _md.convert(content)
        post_date = datetime.now().strftime("%d/%m/%y")

        doc = env.get_template(PAGE_TEMPLATE_FILE).render(
            content=html,
            baseurl=BASE_URL,
            url=url,
            date=post_date,
            **config
        )

        # Writing the post html
        doc = no_p_markdown(doc)
        target_file.write_text(doc, encoding="utf8")


if __name__ == "__main__":
    generate()
