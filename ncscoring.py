import json
import csv

from collections import defaultdict
from operator import itemgetter
from pprint import pprint
from enum import Enum

DEBUG = False

POINTS = [25, 20, 15, 12, 10, 8, 7, 6, 5, 4, 3, 2, 1]
LONG_FILE = "data/long.csv"
RELAY_FILE = "data/relay.csv"

SICSV = {'CLASSIFIER': 12, 'CLUB': 15, 'NATIONALITY': 16, 'CATEGORY': 18, 'PLACE': 43}
SICSV_RELAY = {'CLASSIFIER': 6, 'CLUB': 9, 'NATIONALITY': 10, 'CATEGORY': 12, 'PLACE': -2}

# read config
with open("data/config.json", encoding="utf-8") as config_file:
    CONFIG = json.load(config_file)

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

def read_sicsv(file, categories, sicsv):
    results = defaultdict(list)
    with open(file, encoding="utf-8") as long_file:
        for row in csv.reader(long_file, delimiter=";"):
            if row[sicsv['NATIONALITY']] == "SLO" \
            and row[sicsv['CLASSIFIER']] == Classifier.OK.value \
            and row[sicsv['CATEGORY']] in categories:
                key = (row[sicsv['CATEGORY']])
                value = (int(row[sicsv['PLACE']]), row[sicsv['CLUB']])
                results[key].append(value)

    if DEBUG:
        print("Results with only national clubs")
        pprint(results)
    return results

def calculate_scores(results, runners=2, multiplier=lambda x: 1):
    club_scores = defaultdict(int)
    for category, result in results.items():
        ranking = rank(sorted(result, key=itemgetter(0)))
        counter = defaultdict(int)
        club_cat_scores = defaultdict(int)
        for points, _, club in ranking:
            counter[club] += 1
            if counter[club] <= runners:
                club_cat_scores[club] += points * multiplier(category)
                club_scores[club] += points * multiplier(category)

        if DEBUG:
            print(category)
            pprint(ranking)
            pprint(club_cat_scores)
    if DEBUG:
        print("Sum scores by club")
        pprint(club_scores)
    return club_scores

def score_long(long_file):
    results = read_sicsv(long_file, CONFIG['long'], SICSV)
    return calculate_scores(results)

def relay_multiplier(category):
    return CONFIG['relay']['exceptions'].get(category, CONFIG['relay']['legs'])

def score_relay(relay_file):
    results = read_sicsv(RELAY_FILE, CONFIG['relay']['categories'], SICSV_RELAY)
    return calculate_scores(results, 1, relay_multiplier)

def add_scores(score_dict, sum_dict):
    for k, v in score_dict.items():
        sum_dict[k] += v
    return scores

if __name__ == "__main__":
    scores = defaultdict(int)
    add_scores(score_long(LONG_FILE), scores)
    add_scores(score_relay(RELAY_FILE), scores)

    for club, score in sorted(scores.items(), key=itemgetter(1), reverse=True):
        print("{0:<20s} {1:>5d}".format(club, score))
