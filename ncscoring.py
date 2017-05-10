import json
import csv

from collections import defaultdict
from operator import itemgetter
from pprint import pprint
from enum import Enum

SICSV = {'CLASSIFIER': 12, 'CLUB': 15, 'NATIONALITY': 16, 'CATEGORY': 18, 'PLACE': 43}

class Classifier(Enum):
    OK = '0'
    DNS = '1'
    DNF = '2'
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
    return POINTS[n] if n < len(POINTS) else POINTS[-1]

DEBUG = False
# default
POINTS = [25, 20, 15, 12, 10, 8, 7, 6, 5, 4, 3, 2, 1]
LONG_FILE = "data/long.csv"

# read config
with open("data/config.json", encoding="utf-8") as config_file:
    CONFIG = json.load(config_file)

def read_sicsv(file):
    results = defaultdict(list)
    with open(file, encoding="utf-8") as long_file:
        for row in csv.reader(long_file, delimiter=";"):
            if row[SICSV['NATIONALITY']] == "SLO" \
            and row[SICSV['CLASSIFIER']] == Classifier.OK.value \
            and row[SICSV['CATEGORY']] in CONFIG['long']:
                key = (row[SICSV['CATEGORY']])
                value = (int(row[SICSV['PLACE']]), row[SICSV['CLUB']])
                results[key].append(value)
    if DEBUG:
        print("Results with only national clubs")
        pprint(results)
    return results

def calculate_scores_long(results):
    club_scores = defaultdict(int)
    for category, result in results.items():
        ranking = rank(sorted(result, key=itemgetter(0)))
        counter = defaultdict(int)
        club_cat_scores = defaultdict(int)
        for points, _, club in ranking:
            counter[club] += 1
            if counter[club] <= 2:
                club_cat_scores[club] += points
                club_scores[club] += points

        if DEBUG:
            print(category)
            pprint(ranking)
            pprint(club_cat_scores)
    return club_scores

def score_long(long_file):
    results = read_sicsv(long_file)
    return calculate_scores_long(results)

if __name__ == "__main__":
    scores = score_long(LONG_FILE)
    
    for club, score in sorted(scores.items(), key=itemgetter(1), reverse=True):
        print("{0:<20s} {1:>5d}".format(club, score))
