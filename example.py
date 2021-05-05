# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Example

import os, json
from src.moduleII.SimpleComparator import SimpleComparator

DJROOT = r"data/dowjones"

sc = SimpleComparator()

# Process sample DJ news
files = os.listdir(DJROOT)
for fn in files:
    newsfn = "{}/{}".format(DJROOT, fn)
    with open(newsfn) as json_file:
        data = json.load(json_file)
        news_title = data["Headline"]
        news_body = data["BodyHtml"]

        # News Classify
        result = sc.classify(news_title, news_body)
        print(newsfn, news_title)
        print(result)
