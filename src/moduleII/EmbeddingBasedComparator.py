# encoding=utf-8
# Author: Yu-Lun Chiang
# Description:

import logging
import os
from src.utils.struct import NewsCategory, RetStruct
from src.moduleII.base import BaseComparator

logger = logging.getLogger(__name__)


class EmbeddingBasedComparator(BaseComparator):
    def __init__(self):
        raise NotImplemented

    def classify(self):
        raise NotImplemented

    def evaluate(self):
        raise NotImplemented

    def _load_keywords(self):
        raise NotImplemented

    @property
    def keywords(self):
        raise NotImplemented