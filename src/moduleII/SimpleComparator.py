# encoding=utf-8
# Author: Yu-Lun Chiang
# Description:

import logging
import os
from typing import Union, List, Optional, Tuple
from src.utils import (
    utility as ut,
    struct as st,
)
from src.moduleII.base import BaseComparator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SimpleComparator(BaseComparator):
    """ A Simple Comparator for Business-related News """

    def __init__(
        self,
        nn_keywords: Optional[Union[str, List[str]]] = None,
        esg_keywords: Optional[Union[str, List[str]]] = None,
        load_default: Optional[bool] = True,
    ):
        """
        Init SimpleComparator.

        Args:
            `nn_keywords`: Keywords of Negative News
            `esg_keywords`: Keywords of ESG News
            `load_default`: Whether to load default keywords from src/utils/keywords_file/
        Type:
            `nn_keywords`: string or list of string. It can take "KEYWORDS", ["KEYWORDS1", "KEYWORDS2", ..], "DIR/KEYWORDS.txt" or ["DIR/KEYWORDS.txt", ...]
            `esg_keywords`: string or list of string. Same as `nn_keywords`
            `load_default`: bool
        Return:
            None
        """

        self._nn_keywords = ut.load_keywords(keywords=nn_keywords)
        self._esg_keywords = ut.load_keywords(keywords=esg_keywords)

        if load_default:
            self._load_default()

        self._nn_keywords = list(set(self._nn_keywords))
        self._esg_keywords = list(set(self._esg_keywords))

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

        """ NN """
        nn_score, nn_cnt_drafts = self.evaluate(
            news_title, news_body, self.keywords["nn_keywords"]
        )
        """ ESG """
        esg_score, esg_cnt_drafts = self.evaluate(
            news_title, news_body, self.keywords["esg_keywords"]
        )

        """ Category """
        score = 0.0
        news_category = st.NewsCategory.OTHER
        if nn_score > 0.5 and esg_score < 0.5:
            score = nn_score
            news_category = st.NewsCategory.NN
            matched_keywords = [cnts[0] for cnts in nn_cnt_drafts]
        elif nn_score < 0.5 and esg_score > 0.5:
            score = esg_score
            news_category = st.NewsCategory.ESG
            matched_keywords = [cnts[0] for cnts in esg_cnt_drafts]
        else:
            raise ValueError(
                f"What's the category of the news? nn_score: {nn_score}, esg_score: {esg_score}"
            )

        """ Return """
        ret = st.RetStruct(
            id=0, news_category=news_category, score=score, keywords=matched_keywords
        )
        ret = self.format(ret)
        return ret

    def evaluate(
        self, news_title: str, news_body: str, keywords: List[str]
    ) -> Union[float, List[Tuple[str, int, int]]]:
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
            Score and Matched Details
            rtype1: float
            rtype2: list of tuple
        """

        cnt_drafts = list()
        for keyword in keywords:
            title_cnt = news_title.count(keyword)
            body_cnt = news_body.count(keyword)
            if title_cnt > 0 or body_cnt > 0:
                cnt_drafts.append((keyword, title_cnt, body_cnt))
        cnt_drafts = sorted(cnt_drafts, key=lambda x: (x[1], x[2]), reverse=True)
        score = 0.0
        if len(cnt_drafts) > 0:
            score = 0.5 + 0.01 * len(cnt_drafts)
            if score > 1.0:
                score = 1.0
        return score, cnt_drafts

    @property
    def keywords(self):
        return {
            "nn_keywords": self._nn_keywords,
            "esg_keywords": self._esg_keywords,
        }

    @staticmethod
    def format(input: st.RetStruct) -> dict:
        return {
            "NN": True if input.news_category == input.news_category.NN else False,
            "NN_SCORE": input.score
            if input.news_category == input.news_category.NN
            else 0.0,
            "NN_KEYWORDS": input.keywords
            if input.news_category == input.news_category.NN
            else [],
            "ESG": True if input.news_category == input.news_category.ESG else False,
            "ESG_SCORE": input.score
            if input.news_category == input.news_category.ESG
            else 0.0,
            "ESG_KEYWORDS": input.keywords
            if input.news_category == input.news_category.ESG
            else [],
        }

    def _load_default(self):
        dirname = os.path.join(
            "src",
            "utils",
            "keywords_file",
        )

        """ Default nn keywords file path"""
        nn_file_abs_dirname = os.path.join(
            dirname,
            "negative_news",
        )
        nn_file_path_list = [
            os.path.join(nn_file_abs_dirname, file)
            for file in os.listdir(nn_file_abs_dirname)
            if file.endswith(".txt")
        ]
        nn_default_keywords = ut.load_keywords(nn_file_path_list)
        self._nn_keywords.extend(nn_default_keywords)

        """ Default esg keywords file path"""
        esg_file_abs_dirname = os.path.join(
            dirname,
            "esg",
        )
        esg_file_path_list = [
            os.path.join(esg_file_abs_dirname, file)
            for file in os.listdir(esg_file_abs_dirname)
            if file.endswith(".txt")
        ]
        esg_default_keywords = ut.load_keywords(esg_file_path_list)
        self._esg_keywords.extend(esg_default_keywords)


if __name__ == "__main__":

    import os, json

    DJROOT = r"news_samples/dowjones"

    sc = SimpleComparator()

    files = os.listdir(DJROOT)
    for fn in files:
        newsfn = "{}/{}".format(DJROOT, fn)
        with open(newsfn) as json_file:
            data = json.load(json_file)
            news_title = data["Headline"]
            news_body = data["BodyHtml"]

            result = sc.classify(news_title, news_body)

            print(newsfn, news_title)
            print(result)
            print()
