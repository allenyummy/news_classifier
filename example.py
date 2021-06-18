# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Example

import os, json
from src.utils import struct as st
from src.SimpleComparator import SimpleComparator

DJROOT = r"data/dowjones"
files = os.listdir(DJROOT)

## SimpleComparator
sc1 = SimpleComparator(category="Negative_News")
sc2 = SimpleComparator(category="ESG_News")

for fn in files:
    newsfn = "{}/{}".format(DJROOT, fn)
    with open(newsfn) as json_file:
        data = json.load(json_file)
        news_title = data["Headline"]
        news_body = data["BodyHtml"]

        print(newsfn, news_title)
        print(f"[ TITLE ]: {news_title}")
        print(f"[  BODY ]: {news_body}")

        print("###### Simple Comparator ######")
        res = list()
        for sc in [sc1, sc2]:
            res.append(sc.classify(news_title, news_body))

        sc_ret = st.SpecStruct(
            NN=True if res[0].news_category == st.NewsCategory.NN else False,
            NN_SCORE=res[0].score,
            NN_KEYWORDS=res[0].keywords,
            ESG=True if res[1].news_category == st.NewsCategory.NN else False,
            ESG_SCORE=res[1].score,
            ESG_KEYWORDS=res[1].keywords,
        )
        print(sc_ret)