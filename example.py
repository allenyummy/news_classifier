from news_classifier import biznews

import os, json
DJROOT = r"news_samples/dowjones"

nreader = biznews.init()

# Process sample DJ news 
files = os.listdir(DJROOT)
for fn in files:
    newsfn = "{}/{}".format(DJROOT, fn)
    with open(newsfn) as json_file:
        data = json.load(json_file)
        news_title = data['Headline']
        news_body = data['BodyHtml']

        # News Classify
        result = nreader.classify(news_title, news_body)
        
        print(newsfn, news_title)
        print(result)
