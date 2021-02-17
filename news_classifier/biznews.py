# import json

def init():
    """ init ..."""
    c = NewsReader()
    return c

def classify(news, c):
    """ Classify news """
    return c.classify(news)

class NewsReader():
    """ News Classifier for Business related news."""

    def __init__(self):
        pass

    def classify(self, news_text):

        result = {
            'NN': True,
            'NN_SCORE': 50,
            'ESG': True,
            'ESG_SCORE': 50,
        }
        return result