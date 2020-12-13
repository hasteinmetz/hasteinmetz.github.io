import requests
from bs4 import BeautifulSoup
import json
import math
import sys
import time

def scrape(wikipg, countries, dict):
    # initiliaze to ensure it doesn't carry over
    speakers = "NA"
    places = "NA"
    languagefam = "NA"
    difficulty = "NA"
    wpage = requests.get(url=wikipg)
    wiki = BeautifulSoup(wpage.content, "html.parser")
    title = wiki.find(id='firstHeading').text.encode("UTF-8")
    table = wiki.find("table", {"class":"infobox vevent"})
    wiki = None # to save memory
    if not(table is None):
        for row in table.find_all("tr"):
            if "Native" in row.text:
                if "Native speakers" in row.text:
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
                    geo = row.text[9:len(row.text)].encode("UTF-8").lower().replace(", ",",")
                    geolist = geo.split(",")
                    for pays in countries:
                        for plcs in geolist:
                            if pays==plcs:
                                countryarray.append(pays)
                    if countryarray:
                        places = countryarray
            if "Official" in row.text and "language" in row.text:
                if places == "NA":
                    places = row.text[9:len(row.text)].encode("UTF-8")
            if "region" in row.text:
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
        dict.update({title : {"speakers": speakers, "places":places, "family":languagefam, "difficulty":difficulty}})

def retryfail(failarr, retries, countries, dict):
    for fail in failarr:
        try:
            scrape(fail, countries, dict)
        except:
            if retries > 0:
                failures.append(fail)
                retries -= 1
            else:
                break
                print("TOO MANY RETRIES: ENDING SCRIPT. GOODBYE.")
                exit()

def main():
    starttime = time.time()
    infile = open("languagelinks.txt", "r")
    cfile = open("countries.txt", "r")
    countries = cfile.read().split(",")
    lcount = 0
    retries = 10
    mark = 50
    languagedict = {}
    failures = []
    timearray = []
    for line in infile:
        wikipage = "https://en.wikipedia.org" + line
        wikipage = wikipage[0:len(wikipage)-1]
        try:
            scrapest = time.time()
            scrape(wikipage, countries, languagedict)
            timestamp = time.time() - scrapest
            timearray.append(timestamp)
        except:
            if retries > 0:
                print("Failure:" + wikipage + " retries left: " + str(retries))
                failures.append(wikipage)
                retries -= 1
            else:
                print("TOO MANY RETRIES: ENDING SCRIPT. \n Check your internet connection, or try again later.")
                sys.exit()
        lcount += 1
        if lcount > mark and mark < 800:
            try:
                if mark < 200:
                    avg = 0.5
                else:
                    avg = round(sum(timearray)/len(timearray), 2)
                total = avg*800
                eta = round((total - (time.time() - starttime))/60,2)
                print("~" + str(mark/8) + "% complete" + " | Average request time: " + str(avg) + "s | (Bad) estimate of time left: " + str(eta) + "min.")
                sys.stdout.flush()
            except:
                if mark < 200:
                    avg = 0.5
                else:
                    avg = round(sum(timearray)/len(timearray), 2)
                avg = round(sum(timearray)/len(timearray), 2)
                total = avg*800
                eta = round((total - (time.time() - starttime))/60,2)
                print("~" + str(mark/8) + "% complete" + " | Average request time: " + str(avg) + "s | (Bad) estimate of time left: " + str(eta) + "min.")
            mark += 50
    if failures:
        retryfail(failures, retries, countries, languagedict)
    with open("wikipedia_dump.json",'w') as outfile:
        json.dump(languagedict, outfile, indent=4)
    with open("wikipedia_languages.txt",'w') as outfile:
        for key in languagedict:
            outfile.write("{"+ "\"" + key + "\":" + str(languagedict[key]))
    print("All done! The program may take a moment to finish")

starttime = time.time()
main()
print("Time:" + str(time.time() - starttime))
exit()
