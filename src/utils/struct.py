# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Data Structure

import logging
from typing import List, NamedTuple
import torch
from enum import Enum

logger = logging.getLogger(__name__)


class KeyStruct(NamedTuple):

    id: int
    keyword: List[str]
    score: float
    embedding: torch.tensor

    def __eq__(self, other):
        return self.keyword == other.keyword

    def __repr__(self):
        return f"({self.id}, {self.keyword}), {self.score}, {self.embedding.size()}"


class NewsCategory(Enum):

    NN = "Negative_News"
    ESG = "ESG_News"
    OTHER = "Other"


class RetStruct(NamedTuple):

    id: int
    news_category: NewsCategory
    score: float
    keywords: List[str]

    def __repr__(self):
        return (
            f"[    ID    ]: {self.id}\n"
            f"[ CATEGORY ]: {self.news_category}\n"
            f"[   SCORE  ]: {self.score}\n"
            f"[ KEYWORDS ]: {self.keywords}\n"
        )


class SpecStruct(NamedTuple):

    NN: bool
    NN_SCORE: float
    NN_KEYWORDS: List[str]
    ESG: bool
    ESG_SCORE: float
    ESG_KEYWORDS: List[str]

    def __repr__(self):
        return (
            f"[      NN      ]: {self.NN}\n"
            f"[   NN_SCORE   ]: {self.NN_SCORE}\n"
            f"[  NN_KEYWORDS ]: {self.NN_KEYWORDS}\n"
            f"[      ESG     ]: {self.ESG}\n"
            f"[   ESG_SCORE  ]: {self.ESG_SCORE}\n"
            f"[ ESG_KEYWORDS ]: {self.ESG_KEYWORDS}\n"
        )