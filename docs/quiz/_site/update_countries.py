import urllib2 as api
import json
import csv
from datetime import date

today = str(date.today())

restcountries = "https://restcountries.eu/rest/v2"
ciacountries = "https://raw.githubusercontent.com/iancoleman/cia_world_factbook_api/master/data/factbook.json"

rcountries = api.urlopen(restcountries).read()
rdata=json.loads(rcountries)

ccountries = api.urlopen(ciacountries).read()
cdata=json.loads(ccountries)
del cdata["countries"]["world"]
# add to dictionary when it is people
newdict = {}
counts = {}
for countries in cdata["countries"]:
    if "people" in cdata["countries"][countries]["data"]:
        if "languages" in cdata["countries"][countries]["data"]["people"]:
            newdict.update({countries:"name", countries:cdata["countries"][countries]["data"]["people"]["languages"]})
            counts.update({countries:"nameofcountry"})

with open("country_json_data.txt",'w') as outf:
    json.dump(rdata, outf)

with open("cia_json_data.txt",'w') as outf:
    json.dump(cdata, outf)

with open("pre_languages.txt",'w') as outfile:
    json.dump(newdict, outfile)

with open("countries.json",'w') as outfile:
    json.dump(counts, outfile)

with open("languages.js",'w') as outfile:
    with open("pre_languages.txt",'r') as infile:
        outfile.write("var languages = ")
        for line in infile:
            outfile.write(line)
