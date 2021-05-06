# encoding=utf-8
# Author: Yu-Lun Chiang
# Description:

import logging
import os
from typing import Union, List, Optional
from abc import ABC, abstractmethod
from src.utils import utility as ut

logger = logging.getLogger(__name__)


DEFAULT_DIR_PATH = {
    "Negative_News": "src/utils/keywords_file/negative_news/",
    "ESG_News": "src/utils/keywords_file/esg/",
}


def KeywordsFactory(
    name: str,
    keywords: Optional[Union[str, List[str]]] = None,
    load_default: Optional[bool] = True,
):

    KEYWORDS_LOCALIZERS = {
        "Negative_News": NegativeNewsKeywords,
        "ESG_News": ESGNewsKeywords,
    }
    return KEYWORDS_LOCALIZERS[name](keywords, load_default)


class Keywords(ABC):

    DEFAULT_DIR = None

    def load(
        self,
        keywords: Optional[Union[str, List[str]]] = None,
        load_default: Optional[bool] = True,
    ) -> List[str]:

        ret = list()
        ret.extend(ut.load(keywords))

        if load_default:
            ret.extend(
                ut.load(
                    [
                        os.path.join(self.DEFAULT_DIR, file)
                        for file in os.listdir(self.DEFAULT_DIR)
                        if file.endswith(".txt")
                    ]
                )
            )
        return ret

    @property
    @abstractmethod
    def keywords(self) -> List[str]:
        raise NotImplemented


class NegativeNewsKeywords(Keywords):

    DEFAULT_DIR = DEFAULT_DIR_PATH["Negative_News"]

    def __init__(
        self,
        keywords: Optional[Union[str, List[str]]] = None,
        load_default: Optional[bool] = True,
    ):
        self._keywords = self.load(keywords, load_default)

    @property
    def keywords(self):
        return self._keywords


class ESGNewsKeywords(Keywords):

    DEFAULT_DIR = DEFAULT_DIR_PATH["ESG_News"]

    def __init__(
        self,
        keywords: Optional[Union[str, List[str]]] = None,
        load_default: Optional[bool] = True,
    ):
        self._keywords = self.load(keywords, load_default)

    @property
    def keywords(self):
        return self._keywords