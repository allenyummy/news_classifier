# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Base Keyword Loader for Polymorphism

import logging
import os
from typing import List, Tuple, Union, Optional
from abc import ABC, abstractmethod
from src.utils import utility as ut

logger = logging.getLogger(__name__)


class Keywords(ABC):
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


class BaseKeywordsLoader(Keywords):

    DEFAULT_DIR = None

    def __init__(
        self,
        keywords: Optional[Union[str, List[str]]] = None,
        load_default: Optional[bool] = True,
    ):
        self._keywords = self.load(keywords, load_default)

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
    def keywords(self) -> Tuple[str]:
        return tuple(self._keywords)
