from rich import print
from typer import Exit

from .lib import PageNotFoundException, TooFewLinksException, get_links, get_page_html
from . import app

@app.command()
def psychology(url: str, max_length: int = 15):
    """
    Scrapes the leading hyperlink of Wikipedia pages recursively until the page "Psychology" is reached
    """
    current_url = url
    current_url_split = current_url.split("/")
    print(f"Starting page: {'/'.join(current_url_split[:-1])}[bold red]/{current_url_split[-1]}[/bold red]  [link={current_url}]|Link|[/link]")
    
    flag_reached = False
    print_color = "yellow"
    counter = 0
    while not flag_reached and counter != max_length:
        try:
            current_url = get_links(get_page_html(current_url), 1)[0]
        except PageNotFoundException:
            print("[red]Requested page not found![/red]")
        current_url_split = current_url.split("/")
        
        if current_url == "https://en.wikipedia.org/wiki/Psychology":
            flag_reached = True
            print_color = "green"

        print(f"-> {'/'.join(current_url_split[:-1])}[bold {print_color}]/{current_url_split[-1]}[/bold {print_color}]  [link={current_url}]|Link|[/link]")
        
        counter += 1
    
@app.command()
def scrape(url: str, url_range: int = 10):
    """
    Scrape a Wikipedia page for its hyperlinks. Ignores the topmost note section and links in parenthetical sentences.
    """
    try:
        page_html = get_page_html(url)
    except PageNotFoundException:
        print("[red]Requested page not found![/red]")
        Exit(1)
        
    try:
        link_list = get_links(page_html, url_range)
    except TooFewLinksException as err:
        print("[red]Too many links requested. Printing every link on page.[/red]")
        link_list = err.link_list
        
    print("\n".join(link_list))

if __name__ == "__main__":
    app()