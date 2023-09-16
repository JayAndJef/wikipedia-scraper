from .lib import get_links, get_page_html
from . import app

@app.command()
def psychology(url: str, max_length: int = 15):
    """
    Scrapes the leading hyperlink of Wikipedia pages recursively until the page "Psychology" is reached
    """
    ...
    
@app.command()
def scrape(url: str, range: int = 10):
    """
    Scrape a Wikipedia page for its hyperlinks. Ignores the topmost note section and links in parenthetical sentences.
    """
    get_links(get_page_html(url), range)

if __name__ == "__main__":
    app()