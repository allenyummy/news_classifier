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
from src.utils import struct as st, utility as ut, evaluation as ev
from src.utils.keywords import keywords as ke
from src.moduleII.base import BaseComparator
from src.keyExtractor import keyExtractor

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        ## For keywords of category
        self.word_embedding_model = TransformerWordEmbeddings(embedding_method_or_model)
        ## For document when using the function of evaluate
        self.doc_embedding_model = DocumentPoolEmbeddings([self.word_embedding_model])

        """ Load Keywords of category """
        self.category = category
        self._keywords = ke.KeywordsFactory(
            name=category, keywords=keywords, load_default=load_default
        ).keywords
        self._keywords = list(self._keywords)

        """ Get/Load/Save Keywords Embeddings """
        self._keywords_embeddings = self._load_embeddings(load_cache, cache_dir)
        if save_cache:
            ut.save_embedding(self._keywords_embeddings, cache_dir)

    def classify(
        self,
        news_title: str,
        news_body: str,
        threshold: Optional[float] = 0.6,  # -1.0 <= threshold <= 1.0
        top_n: Optional[int] = 5,
        method: Optional[str] = "doc_based",  # doc_based or key_based
    ):

        news_category, score, most_likely_keywords = self.evaluate(
            news_title, news_body, threshold, top_n, method
        )

        ret = st.RetStruct(
            id=0,
            news_category=news_category,
            score=score,
            keywords=most_likely_keywords,
        )
        return ret

    def evaluate(
        self,
        news_title: str,
        news_body: str,
        threshold: Optional[float] = 0.6,  # -1.0 <= threshold <= 1.0
        top_n: Optional[int] = 5,
        method: Optional[str] = "doc_based",  # doc_based or key_based
    ):

        if method == "doc_based":
            document = news_title
            return self._evaluate_for_document(document, threshold, top_n)
        elif method == "key_based":
            document = f"{news_title}。{news_body}"
            return self._evaluate_for_keywords_of_document(document, threshold, top_n)
        else:
            raise ValueError(
                f"Expected method to be either `doc_based` or `key_based`, but got {method}."
            )

    @property
    def keywords(self) -> Tuple[str]:
        return tuple(self._keywords)

    def keyword_embedding(self, keyword: str):
        ## Be careful to use it. Don't assign value to it.
        ## It only support as a look-up table.
        return self._keywords_embeddings[keyword]

    def _load_embeddings(self, load_cache, cache_dir) -> Dict[str, torch.tensor]:

        keywords_embeddings = dict()
        cache_keywords = list()

        if load_cache:
            cache_dir = os.path.join(cache_dir, self.category.lower())
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

    def _evaluate_for_document(
        self,
        document: str,
        threshold: Optional[float] = 0.6,  # -1.0 <= threshold <= 1.0
        top_n: Optional[int] = 5,
    ) -> Union[st.NewsCategory, float, List[str]]:

        """ Get Document Embedding """
        doc = Sentence(document)
        self.doc_embedding_model.embed(doc)
        doc_embedding = doc.embedding

        """ Scoring """
        ## Get most likely keywords based on cosine similarity, threshold, and top_n
        most_likely = list()
        for keyword, keyword_embedding in self._keywords_embeddings.items():
            cs_score = ev.cosineSimilarity(doc_embedding, keyword_embedding)
            if cs_score >= threshold:
                most_likely.append((keyword, cs_score))

        most_likely = sorted(most_likely, key=lambda k: k[1], reverse=True)
        most_likely = most_likely[: min(top_n, len(most_likely))]
        most_likely_keywords = [element[0] for element in most_likely]

        ## Get average score from most_likely
        sum_score = sum([tmp[1] for tmp in most_likely])
        score = round(sum_score / len(most_likely), 2) if most_likely else 0.0

        """ Category """
        news_category = st.NewsCategory.OTHER
        if score > 0.50:
            if self.category == st.NewsCategory.NN.value:
                news_category = st.NewsCategory.NN
            elif self.category == st.NewsCategory.ESG.value:
                news_category = st.NewsCategory.ESG

        return news_category, score, most_likely_keywords

    def _evaluate_for_keywords_of_document(
        self,
        document: str,
        threshold: Optional[float] = 0.6,  # -1.0 <= threshold <= 1.0
        top_n: Optional[int] = 5,
    ) -> Union[st.NewsCategory, float, List[str]]:

        """ Get Keywords of Document as well as their embeddings """
        keyextractor = keyExtractor(
            tokenization_method_or_model="ckiptagger",
            embedding_method_or_model="ckiplab/bert-base-chinese",
        )
        keywords_of_document = keyextractor.extract_keywords(
            document, n_gram=2, top_n=5
        )[0]

        """ Score """
        ## Get most likely keywords based on cosine similarity, threshold, and top_n
        most_likely = list()
        for keystruct in keywords_of_document:
            for keyword, keyword_embedding in self._keywords_embeddings.items():
                cs_score = ev.cosineSimilarity(keystruct.embedding, keyword_embedding)
                if cs_score >= threshold:
                    most_likely.append((keyword, cs_score))
                    # logger.info(f"{keystruct.keyword} {keyword} {score}")

        most_likely = sorted(most_likely, key=lambda k: k[1], reverse=True)
        ## remove duplicate keywords
        most_likely_remove_dup = list()
        for (keyword, score) in most_likely:
            if keyword not in [element[0] for element in most_likely_remove_dup]:
                most_likely_remove_dup.append((keyword, score))

        most_likely_remove_dup = most_likely_remove_dup[
            : min(top_n, len(most_likely_remove_dup))
        ]
        most_likely_keywords = [element[0] for element in most_likely_remove_dup]

        ## Get average score from most_likely
        sum_score = sum([tmp[1] for tmp in most_likely])
        score = round(sum_score / len(most_likely), 2) if most_likely else 0.0

        """ Category """
        news_category = st.NewsCategory.OTHER
        if score > 0.50:
            if self.category == st.NewsCategory.NN.value:
                news_category = st.NewsCategory.NN
            elif self.category == st.NewsCategory.ESG.value:
                news_category = st.NewsCategory.ESG

        return news_category, score, most_likely_keywords


if __name__ == "__main__":

    ebc = EmbeddingBasedComparator(
        embedding_method_or_model="ckiplab/bert-base-chinese",
        category="Negative_News",
        keywords=None,
        load_default=True,
        load_cache=True,
        save_cache=False,
    )
