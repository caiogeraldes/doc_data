import os
from doc_data.processor import read_data
from doc_data.tools import stanza_doc_to_pandas

PROC_DATA_PATH = "/home/silenus/docs/Academia/Doutorado/data/doc_data/data/"

def test_stanza_to_pandas():
    doc_path = os.path.join(PROC_DATA_PATH,  # type: ignore
                            "Herodotus (0016) - Histories (001).pickle")  # type: ignore
    _, file_name = os.path.split(doc_path)
    author_, doc_name_ = file_name.replace(".pickle", "").split("-")
    author_ = author_.strip()
    doc_name_ = doc_name_.strip()

    stanza_doc_ = read_data(doc_path)
    df = stanza_doc_to_pandas(stanza_doc_, author_, doc_name_)
