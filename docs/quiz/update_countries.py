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
for countries in cdata["countries"]:
    print(cdata["countries"][countries]["data"]["people"])

with open("country_json_data.txt",'w') as outf:
    json.dump(rdata, outf)

with open("cia_json_data.txt",'w') as outf:
    json.dump(cdata, outf)

with open("README.txt",'r') as inf:
    with open("README.txt",'w') as outf:
        for line in inf:
            if "Last updated" in line:
                outf.write(line)
                outf.write("\t" + today)
                break
            else:
                outf.write(line)
