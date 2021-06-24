# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Data Structure

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, NamedTuple, Optional, Tuple, Union

# import torch

logger = logging.getLogger(__name__)


# class KeyStruct(NamedTuple):

#     id: int
#     keyword: List[str]
#     score: float
#     embedding: torch.tensor

#     def __eq__(self, other):
#         return self.keyword == other.keyword

#     def __repr__(self):
#         return f"({self.id}, {self.keyword}), {self.score}, {self.embedding.size()}"


class NewsCategory(Enum):

    NN = "Negative_News"
    ESG = "ESG_News"
    OTHER = "Other"


class RetStruct(NamedTuple):

    id: int
    news_category: NewsCategory
    score: float
    keywords: List[str]
    debug_list: Optional[List[dict]] = list()

    def __repr__(self):
        return (
            f"[    ID    ]: {self.id}\n"
            f"[ CATEGORY ]: {self.news_category}\n"
            f"[   SCORE  ]: {self.score}\n"
            f"[ KEYWORDS ]: {self.keywords}\n"
            f"[   DEBUG  ]: {self.debug_list}\n"
        )


class SpecStruct(NamedTuple):

    NN: bool
    NN_SCORE: float
    NN_KEYWORDS: List[str]
    NN_DEBUG_LIST: List[dict]
    ESG: bool
    ESG_SCORE: float
    ESG_KEYWORDS: List[str]
    ESG_DEBUG_LIST: List[dict]

    def __repr__(self):
        return (
            f"[      NN      ]: {self.NN}\n"
            f"[   NN_SCORE   ]: {self.NN_SCORE}\n"
            f"[  NN_KEYWORDS ]: {self.NN_KEYWORDS}\n"
            f"[   NN_DEBUG   ]: {self.NN_DEBUG_LIST}\n"
            f"[      ESG     ]: {self.ESG}\n"
            f"[   ESG_SCORE  ]: {self.ESG_SCORE}\n"
            f"[ ESG_KEYWORDS ]: {self.ESG_KEYWORDS}\n"
            f"[   ESG_DEBUG  ]: {self.ESG_DEBUG_LIST}\n"
        )


@dataclass
class KeyGenerator_WordStruct:

    topn: int
    threshold: float
    related: List[Tuple[str, float]] = field(default_factory=list)
    debug: str = None

    def __repr__(self):
        return (
            "\n"
            f"[   TOP_N   ]: {self.topn}\n"
            f"[ THRESHOLD ]: {self.threshold}\n"
            f"[  RELATED  ]: {self.related}\n"
            f"[   DEBUG   ]: {self.debug}\n"
        )

    def __2dict__(self):
        return {
            "topn": self.topn,
            "threshold": self.threshold,
            "related": self.related,
            "debug": self.debug,
        }


@dataclass
class KeyGeneratorStruct:

    createtime: str
    modelkey: str
    use_fast: bool
    base: List[str] = field(default_factory=list)
    default_info: Dict[str, Union[int, float]] = field(default_factory=dict)
    force_info: Dict[str, Dict[str, Union[int, float]]] = field(default_factory=dict)
    results: Dict[str, KeyGenerator_WordStruct] = field(default_factory=dict)

    def __repr__(self):
        return (
            "\n"
            f"[  CREATETIME  ]: {self.createtime}\n"
            f"[   MODELKEY   ]: {self.modelkey}\n"
            f"[   USE_FAST   ]: {self.use_fast}\n"
            f"[     BASE     ]: {self.base}\n"
            f"[ DEFAULT_INFO ]: {self.default_info}\n"
            f"[  FORCE_INFO  ]: {self.force_info}\n"
            f"[   RESULTS    ]: See details below.\n"
        ) + ("\n".join(f"{key}: {value}" for key, value in self.results.items()))

    def __2dict__(self):
        return {
            "createtime": self.createtime,
            "modelkey": self.modelkey,
            "ues_fast": self.use_fast,
            "base": self.base,
            "default_info": self.default_info,
            "force_info": self.force_info,
            "results": {
                word: wordstruct.__2dict__()
                for word, wordstruct in self.results.items()
            },
        }
