# Program that scrapes Wikipedia for language information
# 0 arguments scrape the 700+ webpages
# 1 argument opens previous dictionaries and modifies them
# 2 arguments uses a debug list to quickly check if the code works

import requests
from bs4 import BeautifulSoup
import json
import math
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')

def reducebyfunc(predicate, array):
    if not isinstance(array, list):
        return
    if len(array) > 1:
        pos = len(array) - 1
        tmp = predicate(array[pos], array[pos-1])
        tmparray = array[0:pos-1]
        tmparray.append(tmp)
        return reducebyfunc(predicate, tmparray)
    else:
        return array[0]

def speakerstage(speakers):
    try:
        speakers2 = speakers.replace(",", "")
        s = "".join([ c if (c.isalnum() or c==".") else "*" for c in speakers2 ])
        newspeakers = s.split("*")
        return(newspeakers)
    except:
        return("NA")
        print("err-string")

def parsesimplejson(json, key):
    array = []
    for entry in json:
        for k in entry.keys():
            if key in k:
                usethiskey = k
        array.append(entry[usethiskey])
    return(array)

# help from: https://www.geeksforgeeks.org/python-program-for-quicksort/
def quicksort_by_dict(array, dict, euro, value):
    high = len(array) - 1
    if high > 0 and isinstance(array, list):
        med = high
        pivot = array[med]
        if dict[pivot]["continent"] == "Europe" and euro=="T":
            pthing = dict[pivot][value] + 2000000000
        else:
            pthing = dict[pivot][value]
        below = []
        above = []
        for j in range(0, high):
            if dict[array[j]]["continent"] == "Europe" and euro=="T":
                thing = dict[array[j]][value] + 2000000000
            else:
                thing = dict[array[j]][value]
            if thing >= pthing:
                below.append(array[j])
            else:
                above.append(array[j])
        below = quicksort_by_dict(below, dict, euro, value)
        above = quicksort_by_dict(above, dict, euro, value)
        below.append(pivot)
        array = below + above
        return(array)
    else:
        return(array)

def vspeak(speakers):
    def trya(arr):
        if checkf(arr[0]) == "no":
            if checkf(arr[1]) == "no":
                return("NA")
            else:
                return(arr[1])
        else:
            return(arr[0])
    def checkf(n):
        try:
            float(n)
            return("yes")
        except:
            return("no")
    try:
        sp = speakerstage(speakers)
        filtered = filter(lambda x: x!="", sp)
        arr = [];
        v = "NA";
        if "million" in "".join([s.lower() for s in filtered]):
            indices = [i for i, j in enumerate(filtered) if j.lower() == "million"]
            r = ["low", "high"]
            m = min(2, len(indices))
            if m > 1:
                l1 = filtered[indices[0]-1]
                l2 = filtered[indices[1]-1]
                if checkf(l1)=="yes" and checkf(l2)=="yes":
                    if(float(l1)>float(l2)):
                        tmp = l1
                        l1 = l2
                        l2 = tmp
                langs = [l1, l2]
                for l in range(0, m):
                    if checkf(langs[l])=="yes":
                        arr.append(r[l] + ": " + langs[l].encode("utf8") + " million")
                v = arr
            else:
                l = filtered[indices[0]-1]
                if checkf(l)=="yes":
                    v = l + " million"
        else:
            v = trya(filtered)
            if checkf(v)=="no":
                v = "NA"
            if v!="NA" and float(v) > 1000000:
                v = str(round(float(v)/1000000),2) + " million"
        return(v)
    except:
        return("NA")
        print("err-string")

def finddiff(speakers, v):
    try:
        newspeakers = speakerstage(speakers)
        num = newspeakers[0]
        if newspeakers[0] == "":
            num = newspeakers[1]
        number = float(num)
    except:
        return("NA")
        print("err-string")
    if v=="euro":
        mid = 3
        high = 6
    else:
        mid = 50
        high = 100
    if "billion" in speakers.lower():
        return("easy")
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
                if v=="euro":
                    difficulty = "hard"
                else:
                    difficulty = "very hard"
            if number >= 10000 and number < 100000:
                difficulty = "super hard"
            if number >= 0 and number < 10000:
                difficulty = "whizkid"
        return(difficulty)

#find non-latin and rearrange
def findnl(array, stop):
    if isinstance(array, list):
        for el in range(0, len(array)):
            if isinstance(array[el], str) or isinstance(array[el], unicode):
                end = 0
                for char in array[el]:
                    end += 1
                    if end > stop:
                        break
                    if ord(char) > 400:
                        if el==0:
                            return array
                        else:
                            array.insert(0, array.pop(el))
                            return array
    return array

#find non-latin and rearrange
def checknl(line):
    if "Pronunciation" in line:
        line = line.split("Pronunciation")[0]
    elif "pronunciation" in line:
        line = line.split("pronunciation")[0]
    for char in line:
        if ord(char) > 400:
            return True
    return False

def scrape(wikipg, countries, dict):
    # initiliaze to ensure it doesn't carry over
    speakers = "NA"
    vspeakers = "NA"
    places = "NA"
    vplaces = "NA"
    languagefam = "NA"
    difficulty = "NA"
    link = "NA"
    off = "NA"
    region = "NA"
    endonyms = []
    endo = []
    scripts = []
    countrydict = countries["3"]
    cia = countries["1"]
    sam = countries["2"]
    repl = [" ", "\n", "or", ","]
    arabic = ["persian", "arabic", "perso-arabic", "perso", "jawi"]
    stop = "no"
    rowno = 0
    try:
        wpage = requests.get(url=wikipg)
        wiki = BeautifulSoup(wpage.content, "html.parser")
        title = wiki.find(id='firstHeading').text
        table = wiki.find("table", {"class":"infobox vevent"})
        wiki = None # to save memory
    except:
        print("Could not request page: " + wikipg)
        return
    if not(table is None):
        for row in table.find_all("tr"):
            rowno += 1
            if rowno > 5:
                stop = "yes"
            rtext = row.text
            # endonyms
            if stop != "yes" and row.find_all("th")==[] and row.find_all("img")==[]:
                spans = row.find_all("span")
                if spans:
                    for s in spans:
                        if s.has_attr("lang"):
                            endo.append(s.text)
                italics = row.find_all("i")
                for it in range(0, len(italics)):
                    tmp = italics[it].text
                    endo.append(tmp)
                if checknl(rtext):
                    if not(rtext in endo):
                        endo.append(rtext)
            if "Native" in rtext:
                if "Native speakers" in rtext:
                    speakers = rtext[15:len(rtext)]
                    if speakers is None:
                        continue
                    else:
                        vspeakers = vspeak(speakers)
                else:
                    places = rtext[9:len(rtext)]
            if "Official" in rtext and "language" in rtext:
                if places == "NA":
                    places = rtext[9:len(rtext)]
                    offtxt = rtext[9:len(rtext)]
                    offarr = []
                    offgeo = offtxt.lower()
                    for pays in sam:
                        if pays.lower() in offgeo or pays in offgeo:
                            offarr.append(pays)
                    if offarr:
                        off = offarr
            if "region" in rtext:
                if places == "NA":
                    places = rtext[9:len(rtext)]
            if places != "NA":
                countryarray = []
                geo = places.lower()
                for pays in sam:
                    if pays.lower() in geo or pays in geo:
                        countryarray.append(pays)
                if countryarray:
                    vplaces = countryarray
            if "Language family" in rtext:
                languagefam = []
                row2 = row.find("td")
                macrofam = row2.find("div").find("a", href=True)
                if macrofam is None:
                    languagefam.append(row2.text)
                else:
                    languagefam.append(macrofam.text)
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
            if "script" in rtext.lower() or "writing system" in rtext.lower() or "alphabet" in rtext.lower():
                alphabetlinks = row.find_all("a", href=True)
                for alinks in alphabetlinks:
                    linktxt = alinks.text.lower()
                    if not "braille" in linktxt.lower() and not "writing system" in linktxt.lower() and linktxt.lower()!="":
                        if reducebyfunc(lambda x, y : x or y, [a in linktxt.lower() for a in arabic]):
                            scripts.append("Arabic")
                            scripts.append("("+linktxt+")")
                        else:
                            scripts.append(linktxt)
        colonial = ["French", "German", "Portuguese", "English", "Spanish"]
        col = reducebyfunc(lambda x,y : x or y, [c in title for c in colonial])
        if endo:
            endonyms1 = endo
            if not reducebyfunc(lambda x,y : x or y, [t in title for t in ["Serbo", "Serbian", "Vietnamese"]]) and languagefam not in ["Austronesian"]:
                endonyms = findnl(endonyms1, 5)
        else:
            endonyms = "NA"
        if not vplaces == "NA":
            if col:
                euro="T"
            else:
                euro="F"
            vplaces = quicksort_by_dict(vplaces, countrydict, euro, 'population')
            tmpregion = []
            if countrydict and sam:
                for pl in vplaces:
                    if pl in sam:
                        if countrydict[pl]["continent"]:
                            tmpregion.append(countrydict[pl]["continent"])
                            break
            if tmpregion:
                region = tmpregion
        e1 = {"endonym": endonyms, "scripts": scripts, "speakers": speakers, "vspeakers": vspeakers, "places":places, "vplaces":vplaces, "family":languagefam, "link":wikipg, "official":off, "region":region}
        validatefam(e1)
        e1["difficulty"] = finddiff(e1["speakers"], checkdiff(e1, col, countrydict))
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

def checkdiff(thing, col, d):
    if not "mainfam" in thing:
        thing["mainfam"] = "NA"
    if col:
        return("euro")
    easylang = ["Romance", "Germanic", "Slavic", "Uralic", "Slavic", "Baltic", "Celtic"]
    if d:
        if "vplaces" in thing:
            if thing["vplaces"]!= "NA":
                for pl in thing["vplaces"]:
                    if pl in d:
                        if d[pl]["continent"] == "Europe" and thing["mainfam"] in easylang:
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

def switchdict(dic):
    newdic = {}
    for key in dic:
        for lang in dic[key]["languages"]:
            if lang in newdic:
                newdic[lang].append(key)
            else:
                entry = {lang:[key]}
                newdic.update(entry)
    return(newdic)

def scrapeaway(infile, countries):
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
    return(languagedict)

def main():
    starttime = time.time()
    setting = "scrape"
    cfile = open("countries_cia.txt", "r")
    countries1 = cfile.read().split(",")
    cfile = open("countries.json", "r")
    samjson = json.load(cfile)
    countries2 = samjson.keys()
    countries = {"1": countries1, "2": countries2, "3":samjson}
    if len(sys.argv) > 2:
        infile = open("debug.txt", "r")
        setting = "debug"
        print("DEBUG FILE")
        languagedict = scrapeaway(infile, countries)
    elif len(sys.argv) > 1:
        print("NO SCRAPE")
        infile = open("wikipedia_dump.json", "r")
        languagedict = json.load(infile)
        setting = "noscrape"
    else:
        infile = open("languagelinks.txt", "r")
        print("LINKS FILE")
        languagedict = scrapeaway(infile, countries)
    # fix small errors manually in scraper
    if setting != "debug":
        languagedict["Khmer language"]["mainfam"] = "Austroasiatic"
        languagedict["Flemish"]["vplaces"] = ["Belgium"]
        languagedict["Catalan language"]["vplaces"] = ["Spain"]
        languagedict["Persian language"]["vplaces"] = ["Iran", "Afghanistan", "Tajikistan"]
        languagedict["Danish language"]["vplaces"] = ["Denmark"]
        languagedict["English language"]["vplaces"] = "NA"
        khasi = "\xe0\xa6\x95\x20\xe0\xa6\x95\xe0\xa7\x8d\xe0\xa6\xa4\xe0\xa7\x8d\xe0\xa6\xaf\xe0\xa7\x87\xe0\xa6\xa8\x20\xe0\xa6\x96\xe0\xa6\xb8\xe0\xa6\xbf"
        try:
            languagedict["Khasi language"]["endonym"][0] = khasi
        except:
            languagedict["Khasi language"]["endonym"] = [khasi]
        languagedict["Betawi language"]["difficulty"] = "very hard"
        languagedict["German language"]["difficulty"] = "easy"
        languagedict["Hungarian language"]["region"] = "Europe"
        languagedict["Welsh language"]["difficulty"] = "hard"
        languagedict["Irish language"]["difficulty"] = "hard"
        languagedict["Scottish Gaelic"]["difficulty"] = "hard"
        platd = {"endonym": ["Plattd\xc3\xbctsch"],
        "scripts": ["latin"], "speakers": "10 million", "vspeakers": ["10 million"],
        "places":["Germany", "Netherlands"], "vplaces":["Germany", "Netherlands"],
        "family":["Indo-European","Germanic","West Germanic","North Sea Germanic","Low German"],
        "link":"https://en.wikipedia.org/wiki/Low_German", "region": "Europe", "official":"NA"}
        platd["difficulty"] = finddiff(platd["speakers"], checkdiff(platd, True, countries["3"]))
        languagedict.update({"Low German":platd})
    for key in languagedict.keys():
        # corrections for endonyms
        names = languagedict[key]["endonym"]
        if names!="NA":
            if "language" in key:
                lang_english = key.split(" ")[0]
            else:
                lang_english = key
            if isinstance(names, list):
                for n in range(0, len(names)):
                    name = names[n]
                    if "(easy)" not in name:
                        if lang_english in name:
                            names[n] = "(easy) " + names[n]
                    else:
                        pass
            else:
                if "(easy)" not in names:
                    if lang_english in names:
                        names = "(easy) " + names
                else:
                    pass
        # corrections for places
        if languagedict[key]["family"]=="NA":
            languagedict[key]["mainfam"]="NA"
        if languagedict[key]["vplaces"]!="NA":
            noplaces = len(languagedict[key]["vplaces"])
            for place in range(0, noplaces):
                try:
                    pl = languagedict[key]["vplaces"][place]
                    if key[0:2] in pl:
                        tmp = languagedict[key]["vplaces"][0]
                        languagedict[key]["vplaces"][0] = pl
                        languagedict[key]["vplaces"][place] = tmp
                except:
                    pass
        if languagedict[key]["mainfam"]=="Slavic":
            if languagedict[key]["vplaces"]!="NA":
                for place in languagedict[key]["vplaces"]:
                    if place == "Oman":
                        languagedict[key]["vplaces"].remove("Oman")
    with open("wikipedia_dump.json",'w') as outfile:
        json.dump(languagedict, outfile, indent=4)
    if(setting != "debug"):
        with open("languages1.js",'w') as outfile:
            outfile.write("var languages = ")
            json.dump(languagedict, outfile, indent=4)
            outfile.write("\n")
            outfile.write("var listoflanguages = Object.keys(languages);\n")
            outfile.write("var country_js = ")
            cfile_js = open("countries.json", "r")
            country_js = json.load(cfile_js)
            json.dump(country_js, outfile, indent=4)
            outfile.write("\n")
            outfile.write("var lang_js = ")
            lang_js = switchdict(country_js)
            json.dump(lang_js, outfile, indent=4)
            outfile.write("\n")
            outfile.write("var countries = [")
            i = 0
            for c in countries2:
                i += 1
                if i != len(countries2):
                    outfile.write("\n\t" + "\"" + c + "\"" + ",")
                else:
                    outfile.write("\n\t" + "\"" + c + "\"")
            outfile.write("\n];\n")
    print("All done! The program may take a moment to finish")

starttime = time.time()
main()
print("Time:" + str((time.time() - starttime)/60))
exit()
