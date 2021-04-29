# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Evaluation for similarity

import logging
from typing import List
import torch
import torch.nn as nn

logger = logging.getLogger(__name__)

cs = nn.CosineSimilarity(dim=1)


def cosineSimilarity(embedding1: torch.tensor, embedding2: torch.tensor) -> float:
    score = cs(embedding1, embedding2)
    score = score.detach().cpu().numpy()[0]
    return score