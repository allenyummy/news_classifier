# encoding=utf-8
# Author: Yu-Lun Chiang
# Description: keywords extraction

import logging
from typing import List, Union, Optional, Tuple
import torch
from flair.data import Sentence
from flair.embeddings import (
    TransformerWordEmbeddings,
    TransformerDocumentEmbeddings,
    DocumentPoolEmbeddings,
)
from src.utils import (
    tokenization as tk,
    check_input_type_and_transform as ct,
    instantiate as ins,
    stopwords as sw,
    evaluation as ev,
    struct as st,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class keyExtractor:
    def __init__(
        self, tokenization_method_or_model: str, embedding_method_or_model: str
    ):
        self.tokenizer = ins.instantiate_tokenizer(tokenization_method_or_model)
        ## use [CLS] embedding as document embedding
        ## scores are always low.
        # self.document_embedding_model = (
        #     TransformerDocumentEmbeddings(
        #         embedding_method_or_model
        #     )
        # )
        self.word_embedding_model = TransformerWordEmbeddings(embedding_method_or_model)
        self.document_embedding_model = DocumentPoolEmbeddings(
            [self.word_embedding_model]
        )

    def extract_keywords(
        self,
        text: Union[str, List[str], List[List[str]]],
        stopwords: Optional[Union[str, List[str]]] = None,
        is_split_into_words: Optional[bool] = False,
        n_gram: Optional[int] = 1,
        top_n: Optional[int] = 5,
    ) -> List[List[st.KeyStruct]]:

        """ Check and Transform """
        logger.info("===== CHECK AND TRANSFORM =====")
        text = ct.check_input_type_and_transform(text, is_split_into_words)
        logger.info(text)

        """ Tokenize documents """
        logger.info("===== TOKENIZATION =====")
        if not is_split_into_words:
            tokenized_docs = self.tokenizer.tokenize(text)
        else:
            tokenized_docs = text
        logger.info(tokenized_docs)

        """ Get stopwords """
        logger.info("===== GET STOPWORDS ====")
        stopwords_list = sw.get_stopwords(stopwords, add_spacy_stopwords=True)
        logger.info(f"stopwords size: {len(stopwords_list)}")

        """ Get content words by removing stopwords """
        logger.info("===== GET CONTENT WORDS BY REMOVING STOPWORDS =====")
        content_docs = list()
        for tokenized_doc in tokenized_docs:
            content_doc = list()
            for i, token in enumerate(tokenized_doc):
                if token not in stopwords_list:
                    content_doc.append((i, token))
            content_docs.append(content_doc)
        logger.info(content_docs)

        """ Get N-gram """
        logger.info("===== GET N-GRAM =====")
        n_gram_docs = list()
        for doc in content_docs:
            n_gram_doc = list()
            for i in range(len(doc) - n_gram + 1):
                n_gram_doc.append(doc[i : i + n_gram])
            n_gram_docs.append(n_gram_doc)
        logger.info(n_gram_docs)

        """ Get embeddings and calculate score """
        logger.info("===== GET EMBEDDINGS & CALCULATE SCORE =====")
        keyword_lists = list()
        for tokenized_doc, n_gram_doc in zip(tokenized_docs, n_gram_docs):
            doc_embedding = self._get_doc_embedding(tokenized_doc)
            word_embedding_list = self._get_word_embedding_list(
                tokenized_doc, n_gram_doc
            )
            score_list = self.cosineSimilarity(doc_embedding, word_embedding_list)
            keyword_list = self.format(n_gram_doc, word_embedding_list, score_list)
            keyword_list = self.sort(keyword_list)

            ## remove same text list
            keyword_list_remove_dup = list()
            for key in keyword_list:
                if key not in keyword_list_remove_dup:
                    keyword_list_remove_dup.append(key)

            ## top n
            keyword_list_top_n = keyword_list_remove_dup[:top_n]
            keyword_lists.append(keyword_list_top_n)

        for keyword_list in keyword_lists:
            for key in keyword_list:
                logger.info(key)
            logger.info("--")

        return keyword_lists

    def _get_doc_embedding(self, document: List[str]) -> torch.tensor:

        doc = Sentence(document)
        self.document_embedding_model.embed(doc)
        doc_embedding = doc.embedding
        doc_embedding = self._reshape_embedding(doc_embedding)
        return doc_embedding

    def _get_word_embedding_list(
        self, document: List[str], n_gram_doc: List[List[str]]
    ) -> List[torch.tensor]:

        doc = Sentence(document)
        self.word_embedding_model.embed(doc)

        word_embedding_list = list()
        for each_n_gram in n_gram_doc:
            embedding_list = [
                doc[token_idx].embedding for token_idx, token in each_n_gram
            ]
            stack_embedding = torch.stack(embedding_list, dim=0)  ## [N, 768]
            mean_embedding = torch.mean(stack_embedding, dim=0)  ## [1, 768]
            mean_embedding = self._reshape_embedding(mean_embedding)
            word_embedding_list.append(mean_embedding)
        return word_embedding_list

    def _reshape_embedding(self, embedding: torch.tensor) -> torch.tensor:
        return embedding.view(1, -1)  ## [1, 768]

    @staticmethod
    def cosineSimilarity(
        document_embedding: torch.tensor,
        word_embedding_list: List[torch.tensor],
    ) -> List[float]:

        keyword_list = list()
        score_list = list()
        for i, word_embedding in enumerate(word_embedding_list):
            score = ev.cosineSimilarity(document_embedding, word_embedding)
            score_list.append(score)
        return score_list

    @staticmethod
    def format(
        n_gram_doc: List[List[Tuple[int, str]]],
        word_embedding_list: List[torch.tensor],
        score_list: List[float],
    ) -> List[st.KeyStruct]:

        keyword_list = list()
        for i, (each_n_gram, word_embedding, score) in enumerate(
            zip(n_gram_doc, word_embedding_list, score_list)
        ):
            keyword = [token for token_idx, token in each_n_gram]
            keyword = st.KeyStruct(
                id=i, keyword=keyword, score=score, embedding=word_embedding
            )
            keyword_list.append(keyword)
        return keyword_list

    @staticmethod
    def sort(keyword_list: List[st.KeyStruct]) -> List[st.KeyStruct]:
        return sorted(keyword_list, key=lambda k: k.score, reverse=True)


if __name__ == "__main__":

    ke = keyExtractor(
        tokenization_method_or_model="ckiptagger",
        embedding_method_or_model="ckiplab/bert-base-chinese",
    )
    text = "詐欺犯吳朱傳甫獲釋又和同夥林志成假冒檢警人員，向新營市黃姓婦人詐財一百八十萬元，事後黃婦驚覺上當報警處理，匯寄的帳戶被列警示帳戶，凍結資金往返；四日兩嫌再冒名要黃婦領五十萬現金交付，被埋伏的警員當場揪住。"
    text = "報導指出，這起詐騙事件行騙對象主要是馬來西亞華人，嫌犯於2011年7月至9月間撥打6857通馬來西亞電話，詐騙金額人民幣3615.7萬元。"
    text = "晶圓代工龍頭台積電日前核准資本預算28.87億美元，將在中國南京廠擴建28奈米成熟製程產能，卻引起中國通信業分析師項立剛強烈反對，\
            指此舉將打擊中國晶片產業。中國國台辦發言人馬曉光今日表示，相信中國是法治國家，會依法辦事，依法依規來處理。項立剛日前發表「強烈呼籲制止台積電南京廠擴產」一文，\
            稱台積電正在推行高端晶片控制、低端晶片傾銷壓制的策略，呼籲中國官方進行研究、審查，保護中國晶片製造企業，防止台積電的市場壟斷行為。\
            今日在國台辦例行記者會上，有媒體提問，台積電日前宣佈要在南京擴產28奈米全球製程產能帶，中芯國際日前也曾宣佈要在深圳合作擴產28奈米晶片製程，\
            中國有專家表示，台積電擴產或對中芯國際產生排擠競爭效應，還有學者呼籲中國應禁止台積電這個方案，請問對此有何評論？馬曉光則回應，「相信我們是法治國家，會依法辦事，依法依規來處理」。\
            他強調，關於台資台企來中國投資，有完備的法律、法規和管理機制，對於具體個案，有關部門會科學評估，依法依規處理。"
    text = "墾丁悠活麗緻渡假村的三至六區以集合住宅名義興建，目前仍屬停業狀態，僅一、二區共161間房正常營業。屏東縣政府觀光傳播處指出，業者正在辦理使用執照變更成為旅館用途，日前已經通過環評，但仍待墾丁國家公園管理處核准開發許可，最終還需回到縣府申請旅館登記證，屆時才能恢復營業。"
    text = "悠活渡假公司前董事長曾忠信涉及掏空公司資產、詐領資策會補助款及故買盜伐林木等3案件，不法獲益上億元，台南地檢署歷經1年多的偵查，29日將曾忠信等6人依違反證交法、詐欺、背信罪及故買贓物等罪起訴，並請法官從重量刑。"
    keyword_lists = ke.extract_keywords(text, n_gram=1, top_n=10)
