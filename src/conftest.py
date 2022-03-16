import os
import pytest
import stanza


@pytest.fixture(scope="function")
def stanza_resources(tmpdir):
    STANZA_RESOURCES = os.path.join(tmpdir, "stanza_resources")
    stanza.download(lang='grc', model_dir=STANZA_RESOURCES)
    return STANZA_RESOURCES
