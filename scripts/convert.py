import os

from datetime import datetime
from email.utils import formatdate, format_datetime  # for RFC2822 formatting
from pathlib import Path

import jinja2
import markdown
import yaml

import blog

ROOT = Path(__file__).parent.parent

POSTS_DIR = ROOT / "posts"
TEMPLATE_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT

BLOG_TEMPLATE_FILE = "post.html"
INDEX_TEMPLATE_FILE = "index.html"

BASE_URL = os.environ.get("DOMAIN", "http://0.0.0.0:5000/")



def generate_entries():
    posts = POSTS_DIR.glob("*.md")

    extensions = ["extra", "smarty", "meta", "footnotes"]
    loader = jinja2.FileSystemLoader(searchpath=TEMPLATE_DIR)
    env = jinja2.Environment(loader=loader, autoescape=True)

    # retrieving the config infos
    config = yaml.load(Path("config.yaml").read_text(), Loader=yaml.FullLoader)
    config['updatedTime'] = str(datetime.now())


    all_posts = []
    for post in posts:
        print(f"rendering {post}")

        if('template' in str(post)):
            print(f'igoring template: {post}')
            continue

        url = f"{post.stem}.html"
        target_file = OUTPUT_DIR / url

        _md = markdown.Markdown(extensions=extensions, output_format="html5")


        content = post.read_text()
        estimated_reading_time = blog.estimate_reading_time(content)

        html = _md.convert(content)
        _md.Meta['estimated_reading_time']=[estimated_reading_time]

        if _md.Meta.get('publish') == ['no']:
            print('not published')
            continue
        
        doc = env.get_template(str(BLOG_TEMPLATE_FILE)).render(
            content=html,
            baseurl=BASE_URL,
            url=url,
            **_md.Meta,
            **config
        )

        # Writing the post html
        target_file.write_text(doc)

        post_date = datetime.strptime(_md.Meta["published"][0], "%d/%m/%y")
        post_dict = dict(
            **_md.Meta,
            date=post_date,
            rfc2822_date=format_datetime(post_date),
            rel_link=url,
            link="{0}{1}".format(BASE_URL, url),
        )

        all_posts.append(post_dict)

    # Order blog posts by date published
    all_posts.sort(key=lambda item: item["date"], reverse=True)

    with open(OUTPUT_DIR / "index.html", "w") as index_f:
        index_f.write(
            env.get_template(str(INDEX_TEMPLATE_FILE)).render(
                posts=all_posts, template_path=str(BLOG_TEMPLATE_FILE),
                **config
            )
        )


if __name__ == "__main__":
    generate_entries()
