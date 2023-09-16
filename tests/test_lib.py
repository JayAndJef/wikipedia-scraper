import pytest
from wikipedia_scraper.lib import PageNotFoundException, TooFewLinksException, get_page_html, get_links

@pytest.fixture
def page_html():
    with open("tests/wikipedia_source.html") as file:
        return file.read()

def test_request():
    html = get_page_html("https://en.wikipedia.org/wiki/Organism")
    assert b"Organism" in html
    
def test_request_fail():
    with pytest.raises(PageNotFoundException):
        get_page_html("https://en.wikipedia.org/wiki/Goofy_Ani_O")

def test_get_links(page_html):
    links_c = get_links(page_html, 4)
    assert links_c == [
        "https://en.wikipedia.org/wiki/Country_music",
        "https://en.wikipedia.org/wiki/Pop_music",
        "https://en.wikipedia.org/wiki/Nashville_sound",
        "https://en.wikipedia.org/wiki/Countrypolitan"
    ]

def test_link_few_fail(page_html):
    with pytest.raises(TooFewLinksException):
        get_links(page_html, 100000)