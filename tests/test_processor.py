import os
from stanza import Document
from stanza.models.common.doc import Sentence, Word
from doc_data.main import DIORISIS_PATH
from doc_data.processor import gen_data, read_data

PROC_DATA_PATH = "/home/silenus/docs/Academia/Doutorado/data/doc_data/tests/data"
TEST_DOC = "Lysias (0540) - For Callias (005).json"
DIOFILE = os.path.join(DIORISIS_PATH, TEST_DOC)  # type: ignore
OUTNAME = os.path.join(PROC_DATA_PATH, TEST_DOC.replace("json", "pickle"))


def test_gen_data():
    gen_data(DIOFILE, OUTNAME)
    assert(TEST_DOC.replace("json", "pickle") in os.listdir(PROC_DATA_PATH))


def test_read_data():
    doc = read_data(OUTNAME)
    assert(isinstance(doc, Document))
    assert(isinstance(doc.sentences[0], Sentence))
    assert(isinstance(doc.sentences[0].words[0], Word))
