# encoding=utf-8
# Author: Yu-Lun Chiang
# Description:

import logging
import os
from typing import List, Tuple, Union, Optional
from abc import ABC, abstractmethod
from src.utils import utility as ut

logger = logging.getLogger(__name__)


DEFAULT_DIR_PATH = {
    "Negative_News": "src/utils/keywords/negative_news/",
    "ESG_News": "src/utils/keywords/esg/",
}


def KeywordsFactory(
    name: str,
    keywords: Optional[Union[str, List[str]]] = None,
    load_default: Optional[bool] = True,
):

    LOCALIZERS = {
        "Negative_News": NegativeNewsKeywords,
        "ESG_News": ESGNewsKeywords,
    }
    return LOCALIZERS[name](keywords, load_default)


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
    def keywords(self) -> Tuple[str]:
        ## It's not allowed to change self.keywords.
        ## Property decorator makes it impossible to set attribute.
        ## It means we can't assign values to self.keywords. (e.g., self.keywords = XXX)
        ## However, it still can do operations of "append", "remove", "add" and so on.
        ## If type of self.keywords is list or set, we can modify it (e.g., self.keywords.append(XXX)), which shouldn't be allowed.
        ## So, we need to return self.keywords as tuple of string whose feature is that we can't modify elements in self.keywords.
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
    def keywords(self) -> Tuple[str]:
        return tuple(self._keywords)


class ESGNewsKeywords(Keywords):

    DEFAULT_DIR = DEFAULT_DIR_PATH["ESG_News"]

    def __init__(
        self,
        keywords: Optional[Union[str, List[str]]] = None,
        load_default: Optional[bool] = True,
    ):
        self._keywords = self.load(keywords, load_default)

    @property
    def keywords(self) -> Tuple[str]:
        return tuple(self._keywords)