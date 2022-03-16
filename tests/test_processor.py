import os
import stanza
from stanza import Document
from stanza.models.common.doc import Sentence, Word
from doc_data.processor import gen_data, read_data

PROC_DATA_PATH = "/home/silenus/docs/Academia/Doutorado/data/doc_data/tests/data/proc/"
TEST_DOC = "Lysias (0540) - For Callias (005).json"
DIOFILE = os.path.join("/home/silenus/docs/Academia/Doutorado/data/doc_data/tests/data/preproc/", TEST_DOC)  # type: ignore
OUTNAME = os.path.join(PROC_DATA_PATH, TEST_DOC.replace("json", "pickle"))
STANZA_RESOURCES = "./stanza_resources"
stanza.download(lang="grc", model_dir=STANZA_RESOURCES)

def test_gen_data():
    gen_data(DIOFILE, OUTNAME)
    assert(TEST_DOC.replace("json", "pickle") in os.listdir(PROC_DATA_PATH))


def test_read_data():
    doc = read_data(OUTNAME)
    assert(isinstance(doc, Document))
    assert(isinstance(doc.sentences[0], Sentence))
    assert(isinstance(doc.sentences[0].words[0], Word))
