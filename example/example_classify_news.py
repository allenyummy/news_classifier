# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Example

import json
import os

from src.SimpleComparator import SimpleComparator
from src.utils import struct as st

DJROOT = r"data/dowjones"
files = os.listdir(DJROOT)

## SimpleComparator
debug = False
nn_reader = SimpleComparator(category="Negative_News", debug=debug)
esg_reader = SimpleComparator(category="ESG_News", debug=debug)

for fn in files:
    newsfn = "{}/{}".format(DJROOT, fn)
    with open(newsfn) as json_file:
        data = json.load(json_file)
        news_title = data["Headline"]
        news_body = data["BodyHtml"]

        """ INFO """
        print("===========================")
        print(newsfn, news_title)
        print(f"[ TITLE ]: {news_title}")
        print(f"[  BODY ]: {news_body}")
        print("---")

        """ NN """
        nn_res = nn_reader.classify(news_title, news_body)

        """ ESG """
        esg_res = esg_reader.classify(news_title, news_body)

        """ DEBUG DETAILS """
        debug_details = {"NN": nn_res.debug, "ESG": esg_res.debug} if debug else None

        """ Format """
        sc_ret = st.SpecStruct(
            NN=True if nn_res.news_category == st.NewsCategory.NN else False,
            NN_SCORE=nn_res.score,
            NN_KEYWORDS=nn_res.keywords,
            ESG=True if esg_res.news_category == st.NewsCategory.ESG else False,
            ESG_SCORE=esg_res.score,
            ESG_KEYWORDS=esg_res.keywords,
            DEBUG=debug_details,
        )
        print(sc_ret)
