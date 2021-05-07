# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Base Comparator for Polymorphism

import logging
from typing import Tuple
from abc import ABC, abstractmethod


class BaseComparator:
    @abstractmethod
    def classify(self):
        raise NotImplemented

    @abstractmethod
    def evaluate(self):
        raise NotImplemented

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
