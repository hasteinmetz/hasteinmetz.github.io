# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import math

infile = open("languagelinks.txt", "r")
cfile = open("countries.txt", "r")
countries = cfile.read().split(",")
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
            if "region" in row.text:
                if places == "NA":
                    places = row.text[9:len(row.text)].encode("UTF-8")
            if "Native" in row.text:
                if "Native speakers" in row.text:
                    # find not in brackets later
                    # find a way to add stuff
                    speakers = row.text[15:len(row.text)].encode("UTF-8")
                else:
                    # make this an array...
                    # figure out a way to find countries and move through
                    countryarray = []
                    geo = row.text[9:len(row.text)].encode("UTF-8").lower()
                    for pays in countries:
                        if pays in geo:
                            countryarray.append(pays)
                    places = countryarray
            if "Official" in row.text and "language" in row.text:
                if places == "NA":
                    places = row.text[9:len(row.text)].encode("UTF-8")
            if "Language family" in row.text:
                languagefam = []
                row2 = row.find("td")
                macrofam = row2.find("div").find("a", href=True)
                if macrofam is None:
                    languagefam.append(row2.text.encode("UTF-8"))
                else:
                    languagefam.append(macrofam.string)
                tree = row2.find("ul")
                if not(tree is None):
                    trynewthings = tree.find_all(text=True)
                    famarray = []
                    if not(trynewthings is None):
                        for thing in trynewthings:
                            newthing = thing.encode("UTF-8")
                            if newthing != "\n":
                                if "\n" in newthing:
                                    newthing = newthing[1:len(newthing)]
                                famarray.append(newthing)
        languagedict.update({title : {"speakers": speakers, "places":places, "family":languagefam}})
    lcount += 1
    if lcount > mark:
        print(mark, "done")
        mark += 100

with open("wikipedia_dump.json",'w') as outfile:
    json.dump(languagedict, outfile, indent=4)
with open("wikipedia_languages.txt",'w') as outfile:
    for key in languagedict:
        outfile.write("{"+ "\"" + key + "\":" + str(languagedict[key]))
print("all done!")
