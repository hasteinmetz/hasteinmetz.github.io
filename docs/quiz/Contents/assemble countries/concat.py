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

new = {}

if len(pop)!=len(reg) or len(pop)!=len(cont) or len(reg)!=len(cont):
    print("NOT SAME length")
    print(len(pop))
    print(len(reg))
    for i in range(0, len(pop)):
        if pop[i]["country"] != reg[i]["country"]:
            print(pop[i]["country"], i)
            break
else:
    print("PASSED!")

for j in range(0, len(pop)):
    country = pop[j]['country']
    population = pop[j]['population']
    region = reg[j]['location']
    continent = cont[j]['continent']
    entry = {country:{"population":population, "region": region, "continent": continent}}
    new.update(entry)

with open("countries.json",'w') as outfile:
    json.dump(new, outfile, indent=4)
