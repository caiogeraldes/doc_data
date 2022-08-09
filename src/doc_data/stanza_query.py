"""
TODO: make doc_string
"""
from dataclasses import dataclass
from stanza.models.common.doc import Sentence, Word, Document
from typing import Union, List


@dataclass
class LocalToken(Word):
    """
    TODO: make doc_string
    """

    head: int
    sent: Sentence

    def __init__(self, stanza_word=None):
        """
        TODO: make doc_string
        """
        if stanza_word:
            self.__dict__ = stanza_word.__dict__

    def get_head(self) -> Union["LocalToken", None]:
        """
        TODO: make doc_string
        """
        if self.head == 0:
            return None
        return LocalToken(self.sent.words[self.head - 1])

    def get_children(self) -> Union[List["LocalToken"], None]:
        """
        TODO: make doc_string
        """
        children = []
        for token in self.sent.words:
            if token.head == self.id:
                children.append(LocalToken(token))
        if len(children) == 0:
            return None
        return children


@dataclass
class QueryHit:
    """
    TODO: make doc_string
    """

    sentence: Sentence
    hit: LocalToken
    head: Union[None, LocalToken]
    children: List[LocalToken]


def lemma_main_query(doc: Document, constraint: List[str]) -> List[QueryHit]:
    """
    TODO: make doc_string
    """
    query_hits = []

    for sent in doc.sentences:
        for token in sent.words:
            token = LocalToken(token)
            if token.lemma in constraint and token.get_children() is not None:
                query_hits.append(
                    QueryHit(
                        sentence=token.sent,
                        hit=token,
                        head=token.get_head(),
                        children=token.get_children(),
                    )
                )
    return query_hits


def feature_sub_query(
    main_hits: List[QueryHit], constraint: List[str]
) -> List[QueryHit]:
    """
    TODO: make doc_string
    """
    query_hits = []

    for hit in main_hits:
        for child in hit.children:
            if child.feats is None:
                continue
            if any([feat in child.feats.split("|") for feat in constraint]):
                query_hits.append(
                    QueryHit(
                        sentence=child.sent,
                        hit=child,
                        head=child.get_head(),
                        children=child.get_children(),
                    )
                )
    return query_hits
