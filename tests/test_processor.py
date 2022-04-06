import os
import pytest
import stanza
from stanza import Document
from stanza.models.common.doc import Sentence, Word
from doc_data.processor import gen_data, read_data

pytest_plugins = "pytester"

TEST_DOC = "Lysias (0540) - For Callias (005).json"

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")


@pytest.fixture
def stanza_dir(tmpdir):
    stanza_dir = tmpdir.mkdir("stanza_resources")
    return str(stanza_dir)


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, TEST_DOC))
def test_data_tools(stanza_dir, datafiles):
    stanza.download(lang="grc", package="perseus", model_dir=stanza_dir)
    nlp = stanza.Pipeline(
        lang="grc",
        package="perseus",
        verbose=False,
        depparse_batch_size=400,
        dir=stanza_dir,
    )
    diofile: str = str(os.path.join(datafiles, TEST_DOC))
    outfile: str = str(diofile).replace("json", "pickle")
    gen_data(nlp, diofile, outfile)
    assert TEST_DOC.replace("json", "pickle") in os.listdir(FIXTURE_DIR)

    doc: Document = read_data(outfile)
    assert isinstance(doc, Document)
    assert isinstance(doc.sentences[0], Sentence)
    assert isinstance(doc.sentences[0].words[0], Word)
