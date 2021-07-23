# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: SimpleComparator uses keywords to identify negative/esg news.

import logging
import re
from typing import Dict, List, Optional, Tuple, Union

from src.base import BaseComparator
from src.utils import struct as st
from src.utils.keywords import keywords as ke

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SimpleComparator(BaseComparator):
    """A Simple Comparator for Business-related News"""

    def __init__(
        self,
        category: str,  # Only Suppory "Negative_News" and "ESG_News".
        keywords: Optional[Union[str, List[str]]] = None,
        load_default: Optional[bool] = True,
        debug: Optional[bool] = False,
    ):
        """
        Init SimpleComparator.
        SimpleComparator can determine if the news belongs to the category based on keywords.
        It can be regarded as binary classification.

        Args:
            `category`: Category of News that you want to make the program
                        determine if the news belongs to the category or not.
                        Now, it only supports two categories ("Negative_News" or "ESG_News").
            `keywords`: Keywords of News that you think they're important for the category.
                        It can take "KEYWORDS", ["KEYWORDS1", "KEYWORDS2", ..],
                        "DIR/KEYWORDS.txt" or ["DIR/KEYWORDS.txt", ...] as input.
            `load_default`: Whether to load default keywords of the category.
                            It can be seen from src/utils/keywords/keywords.py.
            `debug`: Whether to use debug mode to make sure which sentence contains keywords.
        Type:
            `category`: string.
            `keywords`: string or list of string.
            `load_default`: bool
            `debug`: bool
        Return:
            None
        """

        if category == st.NewsCategory.NN.value:
            self.news_category = st.NewsCategory.NN
        elif category == st.NewsCategory.ESG.value:
            self.news_category = st.NewsCategory.ESG
        else:
            raise ValueError(
                f"Only support either 'Negative_News' or 'ESG_News' category, but got {category}"
            )

        self._keywords = ke.KeywordsFactory(
            name=category, keywords=keywords, load_default=load_default
        ).keywords

        self.debug = debug
        self.id = 0  # Generate id

    def classify(
        self,
        news_title: str,
        news_body: str,
        threshold: float = 0.50,
        title_weight: float = 0.3,
        body_weight: float = 0.1,
    ) -> st.SimpleComparatorStruct:
        """
        Classify News and return classify results.

        Args:
            `news_title`  : Title of news.
            `news_body`   : Content of news.
            `threshold`   : Threshold score to determine if the news belongs to the news category.
            `title_weight`: Weight of news title.
            `body_weight` : Weight of news body.
        Type:
            `news_title`  : string
            `news_body`   : string
            `threshold`   : float
            `title_weight`: float
            `body_weight` : float
        Return:
            A classify result about news
            rtype: st.SimpleComparatorStruct
        """

        score, matched_keywords, debug = self._evaluate(
            news_title, news_body, title_weight, body_weight
        )

        ret = st.SimpleComparatorStruct(
            id=self.id,
            news_category=(
                self.news_category if score > threshold else st.NewsCategory.OTHER
            ),
            score=score,
            keywords=matched_keywords,
            debug=debug if self.debug else None,
        )
        self.id += 1
        return ret

    def _evaluate(
        self,
        news_title: str,
        news_body: str,
        title_weight: float = 0.3,
        body_weight: float = 0.1,
    ) -> Union[float, List[str], List[Dict[str, str]]]:
        """
        Find matched keywords and calculate score.

        Args:
            `news_title`  : Title of news.
            `news_body`   : Content of news.
            `title_weight`: Weight of news title.
            `body_weight` : Weight of news body.
        Type:
            `news_title`  : string
            `news_body`   : string
            `title_weight`: float
            `body_weight` : float
        Return:
            score, matched keywords, debug details
            rtype1: float
            rtype2: list of string
            rtype3: list of Dict[str, str]
        """

        debug = list()

        """ Keywords Matching """
        matched_keywords = list()

        ## news_title
        _, title_matched_keywords, title_total_cnt = self.find_keywords(news_title)
        matched_keywords.extend(title_matched_keywords)
        if title_total_cnt > 0:
            debug.append(
                {
                    "keywords": title_matched_keywords,
                    "text": news_title,
                }
            )

        ## news_body
        body_total_cnt = 0
        for sent in re.findall(r"[^!?。\.\!\?]+[!?。\.\!\?]?", news_body, flags=re.U):

            _, sent_matched_keywords, sent_total_cnt = self.find_keywords(sent)
            matched_keywords.extend(sent_matched_keywords)
            body_total_cnt += sent_total_cnt
            if sent_total_cnt > 0:
                debug.append(
                    {
                        "keywords": sent_matched_keywords,
                        "text": sent,
                    }
                )

        """ Scoring """
        weight = round(title_weight / body_weight, 2)
        matched_keywords_cnt = weight * title_total_cnt + body_total_cnt
        score = self.score_func(matched_keywords_cnt)

        return score, list(set(matched_keywords)), debug

    def score_func(self, matched_keywords_cnt: float) -> float:
        """
        Score function.

        Args:
            `matched_keywords_cnt`: Total count of matched keywords.
        Type:
            `matched_keywords_cnt`: float
        Return:
            score
            rtype: float
        """

        if matched_keywords_cnt == 0:
            return 0.00
        score = 0.50 + 0.50 / (15 ** 2) * (matched_keywords_cnt) ** 2
        return round(score, 2) if score <= 1.00 else 1.00

    def find_keywords(self, text: str) -> Union[List[Tuple[str, int]], List[str], int]:
        """
        Details of finding keywords.

        Args:
            `text`: Input text.
        Type:
            `text`: string
        Return:
            details, matched keywords, count
            rtype1: list of Tuple[str, int]
            rtype2: list of string
            rtype3: integer
        """

        cnt_drafts = list()
        for keyword in self.keywords:
            cnt = text.count(keyword)
            if cnt > 0:
                cnt_drafts.append((keyword, cnt))

        cnt_drafts = sorted(cnt_drafts, key=lambda x: (x[1]), reverse=True)
        matched_keywords = [cnt[0] for cnt in cnt_drafts]
        total_cnt = sum([cnt[1] for cnt in cnt_drafts])
        return cnt_drafts, matched_keywords, total_cnt

    @property
    def keywords(self) -> Tuple[str]:
        """
        Keywords of the news category.
        """

        return tuple(self._keywords)
