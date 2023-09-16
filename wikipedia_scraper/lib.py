import requests
import bs4


class PageNotFoundException(Exception):
    """Raised when a page response is not 200"""

    ...
    
class TooFewLinksException(Exception):
    """Raised when the function requests more then the number of links available on a page"""


def get_page_html(url: str) -> str:
    """Gets the html content of a page

    Args:
        url (str): url of page to get

    Returns:
        str: html of page

    Raises:
        PageNotFoundException
    """
    page_response = requests.get(url)
    if page_response.status_code != 200:
        raise PageNotFoundException

    return page_response.content


def get_links(html: str, range: int) -> list[str]:
    """Gets first <range> links in a wikipedia html document that are not in the note section or in parenthesis

    Args:
        html (str): html of wikipedia page
        range (int): number of links to get

    Returns:
        list[str]: list of links in document
        
    Raises:
        TooFewLinksException
    """
    soup = bs4.BeautifulSoup(html, "html.parser")

    main_content: bs4.Tag = soup.find(id="mw-content-text").find("div")

    for div in main_content.find_all("div"):
        div.decompose()
    for style in main_content.find_all("style"):
        style.decompose()
    for citation in main_content.find_all("sup"):
        citation.decompose()
    for span in main_content.find_all("span"):
        span.decompose()
    for table in main_content.find_all("table"):
        table.decompose()
    for figure in main_content.find_all("figure"):
        figure.decompose()

    for section in list(main_content)[0:10]:
        paren_level = 0
        for child_section in section:
            child_text = ""
            match type(child_section):
                case bs4.element.NavigableString:
                    child_text = child_section
                case bs4.element.Tag:
                    child_text = child_section.text
            if "(" in child_text and ")" in child_text:
                continue
            elif "(" in child_text:
                paren_level += 1
            elif ")" in child_text:
                paren_level -= 1
            if paren_level > 0 and isinstance(child_section, bs4.element.Tag):
                blank = soup.new_tag("b")
                child_section.replace_with(
                    blank
                )  # prevents iterator from skipping a tag due to decomposition
    links = [
        "https://en.wikipedia.org" + l
        for l in [t.get("href") for t in main_content.find_all("a")]
        if "en.wiktionary.org" not in l
    ]
    
    if len(links) < range - 1:
        raise TooFewLinksException(links)

    return links[0:range]
