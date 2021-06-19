# encoding=utf-8
# Author: Yu-Lun Chiang
# Description:

import logging
import os
import re
from typing import Union, List, Optional, Tuple
from src.utils import struct as st
from src.utils.keywords import keywords as ke
from src.base import BaseComparator

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SimpleComparator(BaseComparator):
    """ A Simple Comparator for Business-related News """

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
            `category`: Category of News that you want to make the program to determine if the news belongs to the category or not.
                        Now, it only supports two categories ("Negative_News" or "ESG_News").
            `keywords`: Keywords of News that you think they're important for the category.
                        It can take "KEYWORDS", ["KEYWORDS1", "KEYWORDS2", ..], "DIR/KEYWORDS.txt" or ["DIR/KEYWORDS.txt", ...] as input.
            `load_default`: Whether to load default keywords of the category. It can be seen from src/utils/keywords.py.
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

    def classify(
        self,
        news_title: str,
        news_body: str,
        threshold: float = 0.50,
        title_weight: float = 0.3,
        body_weight: float = 0.1,
    ) -> st.RetStruct:
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

        score, matched_keywords, debug_list = self._evaluate(
            news_title, news_body, title_weight, body_weight
        )

        if score < threshold:
            self.news_category = st.NewsCategory.OTHER

        if self.debug:
            ret = st.RetStruct(
                id=0,
                news_category=self.news_category,
                score=score,
                keywords=matched_keywords,
                debug_list=debug_list,
            )
        else:
            ret = st.RetStruct(
                id=0,
                news_category=self.news_category,
                score=score,
                keywords=matched_keywords,
            )

        return ret

    def _evaluate(
        self,
        news_title: str,
        news_body: str,
        title_weight: float = 0.3,
        body_weight: float = 0.1,
    ) -> Union[float, List[str], dict]:
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

        debug_list = list()

        """ Keywords Matching """
        matched_keywords = list()

        ## news_title
        (
            news_title_cnt_drafts,
            news_title_matched_keywords,
            news_title_total_cnt,
        ) = self._find_keywords(news_title)
        matched_keywords.extend(news_title_matched_keywords)

        if news_title_total_cnt > 0:
            debug_list.append(
                {
                    "keywords": news_title_matched_keywords,
                    "text": news_title,
                }
            )

        ## news_body
        news_body_total_cnt = 0
        for news_body_sent in re.findall(
            "[^!?。\.\!\?]+[!?。\.\!\?]?", news_body, flags=re.U
        ):
            (
                news_body_sent_cnt_drafts,
                news_body_sent_matched_keywords,
                news_body_sent_total_cnt,
            ) = self._find_keywords(news_body_sent)
            matched_keywords.extend(news_body_sent_matched_keywords)
            news_body_total_cnt += news_body_sent_total_cnt

            if news_body_sent_total_cnt > 0:
                debug_list.append(
                    {
                        "keywords": news_body_sent_matched_keywords,
                        "text": news_body_sent,
                    }
                )

        """ Scoring """
        weight = round(title_weight / body_weight, 2)
        total_cnt = weight * news_title_total_cnt + news_body_total_cnt
        score = self._score_func(total_cnt)

        return score, list(set(matched_keywords)), debug_list

    def _score_func(self, keywords_num: float) -> float:
        score = 0.50 + 0.50 / (15 ** 2) * (keywords_num) ** 2
        return round(score, 2) if score <= 1.00 else 1.00

    def _find_keywords(self, text: str) -> Union[List[Tuple[str, int]], List[str], int]:

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
        return tuple(self._keywords)
