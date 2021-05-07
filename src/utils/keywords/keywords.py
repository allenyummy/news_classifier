# encoding=utf-8
# Author: Yu-Lun Chiang
# Description:

import logging
import os
from typing import List, Tuple, Union, Optional
from src.utils.keywords.base import BaseKeywordsLoader

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
        "Negative_News": NegativeNewsKeywordsLoader,
        "ESG_News": ESGNewsKeywordsLoader,
    }
    return LOCALIZERS[name](keywords, load_default)


class NegativeNewsKeywordsLoader(BaseKeywordsLoader):

    DEFAULT_DIR = DEFAULT_DIR_PATH["Negative_News"]

    def __init__(
        self,
        keywords: Optional[Union[str, List[str]]] = None,
        load_default: Optional[bool] = True,
    ):
        super().__init__(keywords, load_default)

    @property
    def keywords(self) -> Tuple[str]:
        return super().keywords


class ESGNewsKeywordsLoader(BaseKeywordsLoader):

    DEFAULT_DIR = DEFAULT_DIR_PATH["ESG_News"]

    def __init__(
        self,
        keywords: Optional[Union[str, List[str]]] = None,
        load_default: Optional[bool] = True,
    ):
        super().__init__(keywords, load_default)

    @property
    def keywords(self) -> Tuple[str]:
        return super().keywords


if __name__ == "__main__":

    nn = NegativeNewsKeywordsLoader(keywords="我")
    print(nn.keywords)

    esg = ESGNewsKeywordsLoader()
    print(esg.keywords)