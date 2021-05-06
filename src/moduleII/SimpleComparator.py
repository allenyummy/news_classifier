# encoding=utf-8
# Author: Yu-Lun Chiang
# Description:

import logging
import os
from typing import Union, List, Optional, Tuple
from src.utils import struct as st
from src.utils.keywords import keywords as ke
from src.moduleII.base import BaseComparator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SimpleComparator(BaseComparator):
    """ A Simple Comparator for Business-related News """

    def __init__(
        self,
        category: str,  # Only Suppory "Negative_News" and "ESG_News".
        keywords: Optional[Union[str, List[str]]] = None,
        load_default: Optional[bool] = True,
    ):
        """
        Init SimpleComparator.
        SimpleComparator can determine if the news belongs to the category based on keywords.
        It can be regarded as binary classification.

        Args:
            `category`: Category of News that you want to make the program to determine if the news belongs to the category or not.
                        Now, it only supports two categories ("Negative_News" or "ESG_News").
            `keywords`: Keywords of News that you think they're important for the category.
                        It can take "KEYWORDS", ["KEYWORDS1", "KEYWORDS2", ..], "DIR/KEYWORDS.txt" or ["DIR/KEYWORDS.txt", ...] as input.
            `load_default`: Whether to load default keywords of the category. It can be seen from src/utils/keywords.py.
        Type:
            `category`: string.
            `keywords`: string or list of string.
            `load_default`: bool
        Return:
            None
        """
        self.category = category
        self._keywords = ke.KeywordsFactory(
            name=category, keywords=keywords, load_default=load_default
        ).keywords

    def classify(self, news_title: str, news_body: str) -> dict:
        """
        Classify News and Return a Dictionary About The News Details.

        Args:
            `news_title`: Title of News
            `news_body`: Content of News
        Type:
            `news_title`: string
            `news_body`: string
        Return:
            a classify result about news
            rtype: dict
        """

        news_category, score, matched_keywords = self.evaluate(news_title, news_body)

        ret = st.RetStruct(
            id=0, news_category=news_category, score=score, keywords=matched_keywords
        )
        return ret

    def evaluate(
        self,
        news_title: str,
        news_body: str,
    ) -> Union[st.NewsCategory, float, List[str]]:
        """
        Find Matched Keywords and Use Them to Calculate Score.

        Args:
            `news_title`: Title of News
            `news_body`: Content of News
            `keywords`: Keywords
        Type:
            `news_title`: string
            `news_body`: string
            `keywords`: list of string
        Return:
            news_category, Score, Matched Keywords
            rtype1: `struct.NewsCategory`
            rtype2: float
            rtype3: list of string
        """

        ## Keywords Matching
        cnt_drafts = list()
        for keyword in self.keywords:
            title_cnt = news_title.count(keyword)
            body_cnt = news_body.count(keyword)
            if title_cnt > 0 or body_cnt > 0:
                cnt_drafts.append((keyword, title_cnt, body_cnt))
        cnt_drafts = sorted(cnt_drafts, key=lambda x: (x[1], x[2]), reverse=True)
        matched_keywords = [cnt[0] for cnt in cnt_drafts]

        ## Scoring
        score = 0.00
        if len(cnt_drafts) > 0:
            score = 0.50 + 0.01 * len(cnt_drafts)
            if score > 1.00:
                score = 1.00
        score = round(score, 2)

        ## Category
        news_category = st.NewsCategory.OTHER
        if score > 0.50:
            if self.category == st.NewsCategory.NN.value:
                news_category = st.NewsCategory.NN
            elif self.category == st.NewsCategory.ESG.value:
                news_category = st.NewsCategory.ESG

        return news_category, score, matched_keywords

    @property
    def keywords(self):
        return self._keywords
