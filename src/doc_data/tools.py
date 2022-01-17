import pandas as pd


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


if __name__ == "__main__":
    import os
    from doc_data.main import PROC_DATA_PATH
    from doc_data.processor import read_data

    doc_path = os.path.join(PROC_DATA_PATH, "Herodotus (0016) - Histories (001).pickle")  # type: ignore
    _, file_name = os.path.split(doc_path)
    author, doc_name = file_name.replace(".pickle", "").split("-")
    author = author.strip()
    doc_name = doc_name.strip()

    stanza_doc = read_data(doc_path)
    df = stanza_doc_to_pandas(stanza_doc, author, doc_name)
    print(df.shape)
    print(df.head())
