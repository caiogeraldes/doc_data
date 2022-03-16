import os
import pytest
import stanza
from stanza import Document
from stanza.models.common.doc import Sentence, Word
from doc_data.processor import gen_data, read_data

PROC_DATA_PATH = "/home/silenus/docs/Academia/Doutorado/data/doc_data/tests/data/proc/"
TEST_DOC = "Lysias (0540) - For Callias (005).json"
DIOFILE = os.path.join("/home/silenus/docs/Academia/Doutorado/data/doc_data/tests/data/preproc/", TEST_DOC)  # type: ignore
OUTNAME = os.path.join(PROC_DATA_PATH, TEST_DOC.replace("json", "pickle"))


@pytest.fixture
def stanza_dir(tmpdir):#, monkeypatch):
    stanza_dir = tmpdir.mkdir("stanza_resources")
    return str(stanza_dir)


def test_gen_data(stanza_dir):
    stanza.download(lang='grc', package="perseus", model_dir=stanza_dir)
    nlp = stanza.Pipeline(lang="grc", package="perseus", verbose=False, depparse_batch_size=400,dir=stanza_dir)
    gen_data(nlp, DIOFILE, OUTNAME)
    assert(TEST_DOC.replace("json", "pickle") in os.listdir(PROC_DATA_PATH))


def test_read_data():
     doc = read_data(OUTNAME)
     assert(isinstance(doc, Document))
     assert(isinstance(doc.sentences[0], Sentence))
     assert(isinstance(doc.sentences[0].words[0], Word))
