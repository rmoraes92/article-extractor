import difflib
from bs4 import BeautifulSoup, Tag

from blog_post_extractor import logger


def match_strings(string1: str, string2: str) -> float:
    """
    Returns a similarity score between two strings.
    """
    seq = difflib.SequenceMatcher(None, string1, string2)
    # ret = seq.ratio()
    # https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher.real_quick_ratio
    ret = seq.real_quick_ratio()
    logger.debug(
        f"Matching strings: [{string1}] and [{string2}] = {ret}"
    )
    return ret


def extract_page_title(html_body) -> str | None:
    """
    Parses the given HTML body, returns the <title> tag content.
    """
    soup = BeautifulSoup(html_body, "html.parser")
    title_tag = soup.head.title
    if title_tag and title_tag.string:
        return title_tag.string.strip()


def extract_blog_post_title_tag(
    title_string: str, html_body: str, match_ratio: float | None = None
) -> Tag | None:
    """
    Parses the given HTML body, returns a tag whose inner text matches the
    title string.
    """
    match_ratio = match_ratio or 0.6
    soup = BeautifulSoup(html_body, "html.parser")

    # Find the first tag in the document whose inner text matches the title
    for tag in soup.body.find_all(recursive=True):
        tag_text = tag.text
        if tag_text and \
                match_strings(tag_text.strip(), title_string) >= match_ratio:
            return tag


def extract_blog_post(html_body: str) -> tuple(str, list[str]):
    """
    Attempts to extract the article text from a certain html page.

    First we try to retrieve the text from  title tag and use to try identify
    where the article starts in the body.

    Once we have a match we proceed to retrieve all the descendant tags
    (recursively).

    Cycle concludes once we reach a footer tag OR the end of tags.
    """

    page_title = extract_page_title(html_body)

    title_tag = extract_blog_post_title_tag(page_title, html_body)

    if not title_tag:
        return page_title, []

    ret = [title_tag.text.strip()]

    for tag in title_tag.find_next_siblings():
        if tag.name == "footer":
            break
        ret.append(tag.text.strip() if tag.text else None)

    return page_title, ret
