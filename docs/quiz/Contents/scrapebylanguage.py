import requests
from bs4 import BeautifulSoup
import json
import math
import sys
import time

def finddiff(speakers, v):
    try:
        speakers2 = speakers.replace(",", "")
        s = "".join([ c if (c.isalnum() or c==".") else "*" for c in speakers2 ])
        newspeakers = s.split("*")[0]
        if newspeakers == "":
            newspeakers = s.split("*")[1]
        number = float(newspeakers)
    except:
        return("NA")
    if v=="euro":
        mid = 3
        high = 6
    else:
        mid = 50
        high = 100
    if "million" in speakers.lower() or number >= 1000000:
        if "million" in speakers.lower() and number > 10000 and number < 1000000:
            number = 1 # handles known exception of Mon Language
        if number >= 1000000:
            number = number/1000000
        if number > 0 and number < 999:
            if number >= 0 and number < mid:
                difficulty = "hard"
            if number >= mid and number < high:
                difficulty = "medium"
            if number >= high and number < 999:
                difficulty = "easy"
        return(difficulty)
    else:
        if number > 0 and number < 1000000:
            if number >= 100000 and number < 1000000:
                difficulty = "very hard"
            if number >= 10000 and number < 100000:
                difficulty = "super hard"
            if number >= 0 and number < 10000:
                difficulty = "whizkid"
        return(difficulty)

def scrape(wikipg, countries, dict):
    # initiliaze to ensure it doesn't carry over
    speakers = "NA"
    places = "NA"
    languagefam = "NA"
    difficulty = "NA"
    link = "NA"
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
                    if speakers is None:
                        continue
                else:
                    countryarray = []
                    geo = row.text[9:len(row.text)].lower().replace(", ",",")
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
                            newthing = thing
                            if newthing != "\n":
                                if "\n" in newthing:
                                    newthing = newthing[1:len(newthing)]
                                famarray.append(newthing)
                    languagefam = languagefam + famarray
                else:
                    languagefam="NA"
        e1 = {"speakers": speakers, "places":places, "family":languagefam, "link":wikipg}
        if e1["languagefam"]=="Austroasiatic\n\nCentral Mon-KhmerKhmer":
            e1["languagefam"]="Austroasiatic"
        validatefam(e1)
        e1["difficulty"] = finddiff(e1["speakers"], checkdiff(e1))
        e2 = {title:e1}
        dict.update(e2)

def changedictvalue(dicti, key, value):
    if key in dicti:
        new_dict = {}
        for keys in dicti:
            if keys == key:
                new_dict[keys] = value
            else:
                new_dict[keys] = dicti[keys]
        return(new_dict)
    else:
        print("ERROR")

def validatefam(e):
    # modify main family according to this list
    fams = ["Semitic", "Bantu", "Slavic", "Baltic", "Romance", "Germanic", "Indo-Aryan", "Iranian", "Algonquian", "Celtic"]
    if "family" in e:
        for lang in e["family"]:
            if lang in fams:
                e["mainfam"] = lang
        if not "mainfam" in e:
            e["mainfam"] = e["family"][0]
    else:
        e["mainfam"] = "NA"

def checkdiff(thing):
    if not "mainfam" in thing:
        thing["mainfam"] = "NA"
    easylang = ["Romance", "Germanic", "Slavic"]
    if thing["mainfam"] in easylang:
        return("euro")
    else:
        return("noneuro")

def retryfail(failarr, retries, countries, dict):
    failures2 = []
    for fail in failarr:
        try:
            scrape(fail, countries, dict)
        except:
            if retries > 0:
                failures2.append(fail)
                retries -= 1
            else:
                break
                print("TOO MANY RETRIES: ENDING SCRIPT. GOODBYE.")
                exit()
    return(failures2)

def main():
    starttime = time.time()
    if len(sys.argv) > 1:
        infile = open("debug.txt", "r")
        print("DEBUG FILE")
    else:
        infile = open("languagelinks.txt", "r")
        print("LINKS FILE")
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
            avg = round(sum(timearray)/len(timearray), 2)
            total = avg*800
            eta = round((total - (time.time() - starttime))/60,2)
            if mark > 200:
                est = "| (Bad) estimate of time left: " + str(eta) + "min."
            else:
                est = ""
            print("~" + str(mark/8) + "% complete" + " | Average request time: " + str(avg) + "s " + est)
            mark += 50
    if failures:
        uhoh = retryfail(failures, retries, countries, languagedict)
    else:
        uhoh=-1
    if uhoh!=-1:
        print("The following languages didn't pass even the second time...:")
        print(str(uhoh))
    with open("wikipedia_dump.json",'w') as outfile:
        json.dump(languagedict, outfile, indent=4)
    with open("languages1.js",'w') as outfile:
        outfile.write("var languages = ")
        json.dump(languagedict, outfile, indent=4)
        outfile.write("\n")
        outfile.write("var listoflanguages = Object.keys(languages);")
    with open("wikipedia_languages.txt",'w') as outfile:
        for key in languagedict:
            outfile.write("{"+ "\"" + key + "\":" + str(languagedict[key]))
    print("All done! The program may take a moment to finish")

starttime = time.time()
main()
print("Time:" + str((time.time() - starttime)/60))
exit()
