# -*- coding: utf-8 -*-

#from .context import aistm
import unittest

from news_classifier import biznews

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def setUp(self):
        self.nreader = biznews.init()

    def test_class_init(self):
        self.assertIsNotNone(self.nreader)
        self.assertTrue(len(self.nreader.nn_keywords) > 0, "No NN keywords loaded")


    def test_classify_return_format(self):
        """ Test the return format of the class.
            The result is a dictionary with format like:
                result = {
                    'NN': nn_flag,
                    'NN_SCORE': nn_score,
                    'NN_KEYWORDS': nn_tokens,
                    'ESG': esg_flag,
                    'ESG_SCORE': esg_score,
                }
        """
        news_title = "this is a title"
        news_body = "this is news body"
        return_keys = ['NN', 'NN_SCORE', 'NN_KEYWORDS', 'ESG', 'ESG_SCORE']

        result = self.nreader.classify(news_title, news_body)
        for k in return_keys:
            self.assertTrue( k in result, "Key '{}' not found in the classify return!".format(k))



if __name__ == '__main__':
    unittest.main()