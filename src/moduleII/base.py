# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Base Comparator for Polymorphism

import logging
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
    def keywords(self):
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def format(self):
        raise NotImplemented
