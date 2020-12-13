# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import math

infile = open("languagelinks.txt", "r")
cfile = open("countries.txt", "r")
countries = cfile.read().split(",")
lcount = 0
retries = 10
mark = 100
languagedict = {}
failures = []

def scrape(wikipg):
    # initiliaze to ensure it doesn't carry over
    speakers = "NA"
    places = "NA"
    languagefam = "NA"
    difficulty = "NA"
    wpage = requests.get(url=wikipg)
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
                    if speakers.find("(") == -1:
                        continue
                    if speakers is None:
                        continue
                    try:
                        newspeakers = speakers.split(" ")[0]
                        diff = newspeakers.replace(",", "")
                        number = float(diff)
                    except:
                        number = -1
                    if "million" in speakers:
                        if number > 0 and number < 999:
                            if number >= 1 and number < 10:
                                difficulty = "hard"
                            if number >= 10 and number < 100:
                                difficulty = "medium"
                            if number >= 100 and number < 999:
                                difficulty = "easy"
                    else:
                        if number > 0 and number < 999999:
                            if number >= 100000 and number < 999999:
                                difficulty = "very hard"
                            if number >= 10000 and number < 99999:
                                difficulty = "super hard"
                            if number >= 1 and number < 10000:
                                difficulty = "whizkid"
                else:
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
                    languagefam = languagefam + famarray
            if isinstance(places, list):
                for pl in places:
                    if title[0:4] in pl:
                        difficulty = "name"
        languagedict.update({title : {"speakers": speakers, "places":places, "family":languagefam, "difficulty":difficulty}})

for line in infile:
    wikipage = "https://en.wikipedia.org" + line
    wikipage = wikipage[0:len(wikipage)-1]
    try:
        scrape(wikipage)
    except:
        if retries > 0:
            failures.append(wikipage)
            retries -= 1
        else:
            break
            print("TOO MANY RETRIES: ENDED SCRIPT")
    lcount += 1
    if lcount > mark:
        print(mark, "done")
        mark += 100

for fail in failures:
    try:
        scrape(wikipage)
    except:
        if retries > 0:
            failures.append(wikipage)
            retries -= 1
        else:
            break
            print("TOO MANY RETRIES: ENDED SCRIPT")
            quit()

with open("wikipedia_dump.json",'w') as outfile:
    json.dump(languagedict, outfile, indent=4)
with open("wikipedia_languages.txt",'w') as outfile:
    for key in languagedict:
        outfile.write("{"+ "\"" + key + "\":" + str(languagedict[key]))
print("all done!")
quit()
