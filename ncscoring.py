# my imports
import json
import csv
from enum import Enum
from operator import itemgetter
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

def rank(iterable):
    ranked_list = []
    last_result, last_rank = None, None
    for n, item in enumerate(iterable):
        if item[0] == last_result:
            ranked_list.append((get_points(last_rank),) + item)
        else:
            ranked_list.append((get_points(n),) + item)
            last_result, last_rank = item[0], n
    return ranked_list

def get_points(n):
    return POINTS[n] if n < len(POINTS) else 1

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
           and row[SICsv.CLASSIFIER] == Classifier.OK.value \
           and row[SICsv.CATEGORY] in CONFIG['long']:
            key = (row[SICsv.CATEGORY])
            value = (int(row[SICsv.PLACE]), row[SICsv.CLUB])
            results[key].append(value)

results = {category: rank(sorted(result, key=itemgetter(0)))
           for category, result in results.items()}

club_cat_scores = defaultdict(int)
club_scores = defaultdict(int)

for category, ranking in results.items():
    # ranking = rank(sorted(result, key=itemgetter(0)))
    counter = defaultdict(int)
    for points, _, club in ranking:
        counter[club] += 1
        if counter[club] <= 2:
            key = (category, club)
            club_cat_scores[key] += points
            club_scores[club] += points 

