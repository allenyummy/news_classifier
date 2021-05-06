# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Example

import os, json
from src.utils.utility import format
from src.moduleII.SimpleComparator import SimpleComparator

DJROOT = r"data/dowjones"

sc1 = SimpleComparator(category="Negative_News")
sc2 = SimpleComparator(category="ESG_News")

files = os.listdir(DJROOT)
for fn in files:
    newsfn = "{}/{}".format(DJROOT, fn)
    with open(newsfn) as json_file:
        data = json.load(json_file)
        news_title = data["Headline"]
        news_body = data["BodyHtml"]

        res = list()
        for sc in [sc1, sc2]:
            res.append(sc.classify(news_title, news_body))

        print(newsfn, news_title)
        print(format(res))
        print()
