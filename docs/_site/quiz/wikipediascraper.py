import requests
from bs4 import BeautifulSoup

# consulted: https://www.freecodecamp.org/news/scraping-wikipedia-articles-with-python/

page = "https://en.wikipedia.org/wiki/Index_of_language_articles"
wikipage = requests.get(url=page)
wikilist = BeautifulSoup(wikipage.content, "html.parser")
links = wikilist.find_all('td')

with open("languagelinks.txt", "w") as outfile:
    for i in links:
        link = i.find('a',href=True)
        if link is None:
            continue
        if link.find("/wiki/") == -1:
            continue
        if "php" in link["href"] or "index" in link["href"] or "/w/" in link["href"] or "category" in link["href"]:
            continue
        else:
            if "languages" in link["href"]:
                continue
            if "language" in link["href"]:
                outfile.write(link["href"])
                outfile.write("\n")
