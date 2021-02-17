from news_classifier import biznews

news_text = "this is a news...."

c = biznews.init()
result = biznews.classify(news_text, c)

print(result)
