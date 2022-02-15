"""
Helper functions for converting stanza documents into
pandas dataframes.
"""
import pandas as pd  # type: ignore


def stanza_doc_to_pandas(stanza_doc, author: str, doc_name: str) -> pd.DataFrame:
    """docstring for stanza_doc_to_pandas"""

    words = []
    for sent_id, sentence in enumerate(stanza_doc.to_dict()):
        for word in sentence:
            word["sent_id"] = sent_id + 1
            word["author"] = author
            word["doc_name"] = doc_name
            words.append(word)

    return pd.DataFrame(words)
