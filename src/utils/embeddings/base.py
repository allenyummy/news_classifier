# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Base Embedding Loader

import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseEmbeddingsLoader(ABC):


    @property
    @abstractmethod
    def embeddings(self) -> torch.tensor:
        raise NotImplemented