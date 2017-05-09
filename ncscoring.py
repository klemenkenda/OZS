# my imports
import json
import csv
from enum import Enum
from collections import defaultdict

class SICsv():
    CLASSIFIER = 12
    CLUB = 15
    NATIONALITY = 16
    CATEGORY = 18
    PLACE = 43

class Classifier(Enum):
    OK = '0'
    DNS = '1'
    MP = '3'

# default
POINTS = [25, 20, 15, 12, 10, 8, 7, 6, 5, 4, 3, 2, 1]
LONG_FILE = "data/long.csv"

# read config
with open("data/config.json", encoding="utf-8") as config_file:
    CONFIG = json.load(config_file)

results = defaultdict(list)

with open(LONG_FILE, encoding="utf-8") as long_file:
    for row in csv.reader(long_file, delimiter=";"):
        if row[SICsv.NATIONALITY] == "SLO" \
           and row[SICsv.CLASSIFIER] == Classifier.OK.value:
            key = (row[SICsv.CATEGORY])
            value = (int(row[SICsv.PLACE]), row[SICsv.CLUB])
            results[key].append(value)
