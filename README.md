# WikiPsy
[![PyPI version](https://badge.fury.io/py/wikipsy.svg)](https://badge.fury.io/py/wikipsy)

Provides multiple functionalities for scraping wikipedia, the centerpoint being getting to psychology.

## Installation

Use pip:
```sh
pip install wikipsy
```

And then run 
```
❯ wikipsy --help
                                                                                                                                                                                          
 Usage: wikipsy [OPTIONS] COMMAND [ARGS]...                                                                                                                           
                                                                                                                                                                                          
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                                │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                                         │
│ --help                        Show this message and exit.                                                                                                                              │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ graph-multiple  Given multiple wikipedia pages, scrapes and generated a directed graphviz source file showing the those articles' path to Psychology. For ease of use, direct the      │
│                 output of this command into a graphviz dot file.                                                                                                                       │
│ psychology      Scrapes the leading hyperlink of Wikipedia pages recursively until the page "Psychology" is reached.                                                                   │
│ scrape          Scrape a Wikipedia page for its hyperlinks. Ignores the topmost note section and links in parenthetical sentences.                                                     │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```