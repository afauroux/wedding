# blog.py

import re
from pathlib import Path

WPM = 200
WORD_LENGTH = 5
PIC_TIME = 0.3 # min


def _count_words_in_text(text: str) -> int:
    return len(text) // WORD_LENGTH


def _filter_visible_text(text: str) -> str:
    remove_header = re.compile("---.*\.\.\.",re.DOTALL)
    clear_html_tags = re.compile("<.*?>")
    clear_images = re.compile("!\[(.*?)\]\(.*?\)")
    clear_images2 = re.compile("\[.*?\]:\s?.*")
    clear_jumps = re.compile("\n+")
    text = re.sub(remove_header, "", text)
    text = re.sub(clear_html_tags, "", text)
    text = re.sub(clear_images, "", text)
    text = re.sub(clear_images2, "", text)
    text = re.sub(clear_jumps, "\n", text)
    return "".join(text.split())

def _count_pics(text: str) -> float:
    m = re.compile("!\[(.*?)\]\(.*?\)")
    npics = len(re.findall(m,text))
    return npics*PIC_TIME

def estimate_reading_time(text: str) -> int:
    filtered_text = _filter_visible_text(text)
    total_words = _count_words_in_text(filtered_text)
    time = total_words / WPM + _count_pics(text)
    return max(round(time), 1)


if __name__=="__main__":
    ROOT = Path(__file__).parent.parent

    POSTS_DIR = ROOT / "posts"
    posts = POSTS_DIR.glob("*.md")

    for post in posts:
        print(post)
        print(estimate_reading_time(post.read_text()))