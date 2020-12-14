# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import math

infile = open("languagelinks.txt", "r")
lcount = 0
mark = 100
languagedict = {}
for line in infile:
    # initiliaze to ensure it doesn't carry over
    speakers = "NA"
    places = "NA"
    wikipage = "https://en.wikipedia.org" + line
    wikipage = wikipage[0:len(wikipage)-1]
    wpage = requests.get(url=wikipage)
    wiki = BeautifulSoup(wpage.content, "html.parser")
    title = wiki.find(id='firstHeading').text.encode("UTF-8")
    table = wiki.find("table", {"class":"infobox vevent"})
    if not(table is None):
        for row in table.find_all("tr"):
            if "Native" in row.text:
                if "Native speakers" in row.text:
                    # find not in brackets later
                    # find a way to add stuff
                    speakers = row.text[15:len(row.text)].encode("UTF-8")
                else:
                    # make this an array...
                    places = row.text[9:len(row.text)].encode("UTF-8")
        if not(speakers="NA" and places="NA"):
            languagedict.update({title : {"speakers": speakers, "places":places}})
    lcount += 1
    if lcount > mark:
        print(mark, "done")
        mark += 100

with open("wikipedia_languages.json",'w') as outfile:
    json.dump(languagedict, outfile, indent=4)
with open("wikipedia_languages.txt",'w') as outfile:
    for key in languagedict:
        outfile.write("{"+ "\"" + key + "\":" + str(languagedict[key]))
print("all done!")