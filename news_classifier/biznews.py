# import json

def init():
    """ Create an object and init it. Make it as a function as we may need to config something."""
    c = NewsReader()

    # May need to assign/setup the class, e.g.,
    MODEL_PATH = r'data/model'
    c.model = MODEL_PATH
    
    return c

class NewsReader():
    """ News Classifier for Business related news."""

    def __init__(self):
        pass

    def classify(self, news_text):
        """Gets and prints the spreadsheet's header columns

        Parameters
        ----------
        nets_text : str
            The target news content as a string.

        Returns
        -------
        dict
            News classify result. 
        """

        result = {
            'NN': True,
            'NN_SCORE': 50,
            'ESG': True,
            'ESG_SCORE': 50,
        }
        return result