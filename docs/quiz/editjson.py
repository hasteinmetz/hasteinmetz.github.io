import requests
import json
import math

infile = open("wikipedia_dump.json", "r")
wiki = json.load(infile)
cfile = open("countries.txt")
countries = cfile.split(",")

for key in wiki:
    for pop in wiki["key"]["speakers"]:
        # replace "\u00a0"
        # get rid of initial bracket
        # CHECK FOR LARGE L2 (Swahili esp.)
    for loc in wiki["key"]["places"]:
