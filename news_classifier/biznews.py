from news_classifier import config

def init():
    """ Create an object and init it. Make it as a function as we may need to config something."""
    c = NewsReader()
    c.load_NN_keywords()

    # Fixme: we may need to load NN_Keywords from a file?
    # NN_KEYWORDS = r'docs/NN_keywords.txt'
    # c.load_NN_keywords_fromfile(NN_KEYWORDS)

    return c

class NewsReader():
    """ News Classifier for Business related news."""

    def __init__(self):
        self.nn_keywords = []
        
    def load_NN_keywords(self):
        """Load (user defined) NN Keywords from config."""
        self.nn_keywords = config.NN_KEYWORDS

    def load_NN_keywords_fromfile(self, nn_filename):
        """Load (user defined) NN Keywords from text file. (UTF-8 encoding)
            File Info:
                Encoding: UTF-8
                Format: Each line = 1 key words
        """
        wordlist = []
        with open(nn_filename, 'r') as nnfile:
            for line in nnfile:
                pharse = line.rstrip()
                assert len(pharse.split()) == 1, "Wrong File format"
                wordlist.append(pharse)
        print("# NN Keywords loaded: ", len(wordlist))
        self.nn_keywords = wordlist

    def classify(self, news_title, news_body):
        """Gets and prints the spreadsheet's header columns

        Parameters
        ----------
        news_title: str
            The title of the news as a string.
        news_body: str
            The content of the news as a string.

        Returns
        -------
        dict
            News classify result. 
        """

        nn_flag = False
        nn_score = 0
        nn_tokens = []

        esg_flag = False
        esg_score = 0

        # TODO: Move this to another function?
        # Count how many NN words exists in the news (title/body)
        cnt_drafts = []
        for nn_word in self.nn_keywords:
            title_cnt = news_title.count(nn_word)
            body_cnt = news_body.count(nn_word)
            if (title_cnt > 0 ) or (body_cnt > 0):
                cnt_drafts.append((nn_word, title_cnt, body_cnt))
                nn_flag = True

        # Generate matched NN keywords
        cnt_drafts = sorted(cnt_drafts, key = lambda x: (x[1], x[2]), reverse=True)
        for cnts in cnt_drafts:
            # return keywords + cnt for debugging
            #nn_tokens.append((cnts[0], cnts[1]+cnts[2]))
            nn_tokens.append(cnts[0])

        # FIXME: we may need a better way to evaluate the NN score 
        # For now, just implement a simple function as placeholder.
        if len(cnt_drafts) > 0:
            nn_score = 80 + 5 * len(cnt_drafts)
            if nn_score > 100: nn_score = 100

        result = {
            'NN': nn_flag,
            'NN_SCORE': nn_score,
            'NN_KEYWORDS': nn_tokens,
            'ESG': esg_flag,
            'ESG_SCORE': esg_score,
        }
        return result