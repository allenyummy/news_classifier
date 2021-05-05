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