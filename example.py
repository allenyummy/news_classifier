from news_classifier import biznews

newslist = [
    "this is news 1. bla bla bla bla....",
    "this is another news article. foo bar 123"
]

nreader = biznews.init()

for news in newslist:
    result = nreader.classify(news)
    print(result)
