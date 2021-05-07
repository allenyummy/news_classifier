# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: Embedding-based Comparator

import logging
import os
from typing import List, Dict, Set, Tuple, Union, Optional
import torch
from flair.data import Sentence
from flair.embeddings import (
    TransformerWordEmbeddings,
    TransformerDocumentEmbeddings,
    DocumentPoolEmbeddings,
)
from src.utils import struct as st, utility as ut
from src.utils.keywords import keywords as ke
from src.moduleII.base import BaseComparator

logger = logging.getLogger(__name__)


class EmbeddingBasedComparator(BaseComparator):
    def __init__(
        self,
        embedding_method_or_model: str,
        category: str,
        keywords: Optional[Union[str, List[str]]] = None,
        load_default: Optional[bool] = True,
        load_cache: Optional[bool] = True,
        save_cache: Optional[bool] = False,
        cache_dir: Optional[str] = "model/keywords/",
    ):
        """ Init TransformerWordEmbeddings model """
        self.word_embedding_model = TransformerWordEmbeddings(embedding_method_or_model)

        """ Load Keywords """
        self.category = category
        self._keywords = ke.KeywordsFactory(
            name=category, keywords=keywords, load_default=load_default
        ).keywords

        """ Get/Load/Save Keywords Embeddings """
        self._keywords_embeddings = self._load_embeddings(load_cache, cache_dir)
        if save_cache:
            ut.save_embedding(self._keywords_embeddings, cache_dir)

    def classify(self):
        raise NotImplemented

    def evaluate(self):
        raise NotImplemented

    @property
    def keywords(self) -> Tuple[str]:
        return tuple(self._keywords)

    def keyword_embedding(self, keyword: str):
        return self._keywords_embeddings[keyword]

    def _load_embeddings(self, load_cache, cache_dir) -> Dict[str, torch.tensor]:

        keywords_embeddings = dict()
        cache_keywords = list()

        if load_cache:
            if not os.path.exists(cache_dir):
                raise ValueError(f"{cache_dir} is not found.")
            cache_keywords = [file.split(".")[0] for file in os.listdir(cache_dir)]
            self._keywords.extend(
                [
                    cache_keyword
                    for cache_keyword in cache_keywords
                    if cache_keyword not in self._keywords
                ]
            )

        for keyword in self.keywords:
            ## IF load_cache, THEN cache_keywords is [].
            if keyword in cache_keywords:
                file = f"{keyword}.pt"
                word_embedding = torch.load(os.path.join(cache_dir, file))
            else:
                word_embedding = ut.get_word_embedding(
                    self.word_embedding_model, keyword
                )
            keywords_embeddings[keyword] = word_embedding

        return keywords_embeddings


if __name__ == "__main__":

    ebc = EmbeddingBasedComparator(
        embedding_method_or_model="ckiplab/bert-base-chinese",
        category="Negative_News",
        keywords=None,
        load_default=True,
        load_cache=True,
        save_cache=False,
    )
    print(ebc.keywords)
    print(ebc.keyword_embedding("人口販賣"))
