import json
import math
import sys
import time

cfile = open("country_pop.json", "r")
pop = json.load(cfile)
cfile = open("country_region.json", "r")
reg = json.load(cfile)
cfile = open("country_cont.json", "r")
cont = json.load(cfile)
cfile = open("country_languages_samayo.txt", "r")
lang = json.load(cfile)

new = {}

files = [pop, reg, cont, lang]

def newarray(array, index):
    end = len(array)
    if index > end or index < 0:
        print("newarray(%d): error" % index)
    else:
        if index == 0:
            arr = array[1:end]
            return arr
        if index == end:
            arr = array[0:end-1]
            return arr
        else:
            arr = array[0:index] + array[index+1:end]
            return arr

def findtrue(array):
    for i in range(0, len(array)-1):
        tmp = newarray(array, i)
        for j in range(0, len(tmp)-1):
            if len(array[i]) != len(tmp[j]):
                return(False)
    return(True)

def checkfiles(f1, f2):
    for k in range(0, len(f1)-1):
        for l in range(0, len(f2)-1):
            if f1[k] != f2[l]:
                print(f1[k], f2[l])
                return

if not findtrue(files):
    print("NOT SAME length")
    print(len(files))
    for f in files:
        print(len(f))
    for i in range(0, len(files)-1):
        tmp = newarray(array, i)
        for j in range(0, len(tmp)-1):
            f1 = files[i]
            f2 = tmp[j]
            checkfiles(f1, f2)
else:
    print("PASSED!")

def find_in_json(dict, co, key):
    for i in dict:
        if co == i["country"]:
            return(i[key])
    return("NA")

for j in range(0, len(pop)):
    country = pop[j]['country']
    population = pop[j]['population']
    region = find_in_json(reg, country, "location")
    continent = find_in_json(cont, country, "continent")
    languages = find_in_json(lang, country, "languages")
    entry = {country:{"population":population, "region": region, "continent": continent, "languages": languages}}
    new.update(entry)

with open("countries.json",'w') as outfile:
    json.dump(new, outfile, indent=4)
