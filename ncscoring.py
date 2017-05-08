# my imports
import json
import csv
import sys
from pprint import pprint

# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# print(sys.stdout.encoding)

# default
POINTS = [25, 20, 15, 12, 10, 8, 7, 6, 5, 4, 3, 2, 1]


# read config
with open("data/config.json", encoding="utf-8") as config_file:
    CONFIG = json.load(config_file)

# evaluate long
with open("data/long.csv", encoding="utf-8") as long_file:
    csvreader = csv.reader(long_file, delimiter=";", quotechar='"')
    for row in csvreader:
        print(", " . join(row))

# evaluate relay

# output report
pprint(CONFIG["long"])