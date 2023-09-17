from rich import print
from typer import Exit
import graphviz

from .lib import PageNotFoundException, TooFewLinksException, get_links, get_page_html
from . import app

@app.command()
def psychology(url: str, max_length: int = 15):
    """
    Scrapes the leading hyperlink of Wikipedia pages recursively until the page "Psychology" is reached.
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
def graph_multiple(urls: list[str], max_length: int = 15, verbose: bool = False):
    """
    Given multiple wikipedia pages, scrapes and generated a directed graphviz source file showing the those articles' path to Psychology.
    For ease of use, direct the output of this command into a graphviz dot file.
    """
    graph = graphviz.Digraph()

    for url in urls:
        current_url = url
        current_url_name = current_url.split("/")[-1]
        graph.node(current_url.replace("https://", ""), current_url_name)
        
        flag_reached = False
        counter = 0
        while not flag_reached and counter != max_length:
            old_url = current_url
            
            try:
                current_url = get_links(get_page_html(current_url), 1)[0]
            except PageNotFoundException:
                print("[red]A requested page was not found![/red]")
            
            current_url_name = current_url.split("/")[-1]
            current_url_right = current_url.replace("https://", "")
            graph.node(current_url_right, current_url_name)
            graph.edge(old_url.replace("https://", ""), current_url_right)
            
            if verbose:
                print(f"[yellow]{old_url}[/yellow] -> [yellow]{current_url}[/yellow]")
            
            if current_url == "https://en.wikipedia.org/wiki/Psychology":
                if verbose:
                    print("[green]Source reached Psychology[/green]")
                break
            counter += 1
            
    print("Graphviz source:")
    print(graph.source)
    
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