from news_classifier import biznews

news_text = "this is a news...."

nreader = biznews.init()
result = nreader.classify(news_text)

print(result)
