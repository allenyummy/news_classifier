# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Data Structure

import logging
from typing import List, NamedTuple
import torch

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