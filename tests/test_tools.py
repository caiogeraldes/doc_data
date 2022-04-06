import os
import pytest
from doc_data.db import mongo, write_pickle_to_mongo
from doc_data.tools import gen_sent

MONGO = "mongodb+srv://pytest:1234@pytest.ckrsn.mongodb.net/pytest?retryWrites=true&w=majority"

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR))
def test_independent_query(datafiles):
    PROC_DATA_PATH = str(datafiles)
    db = mongo(MONGO, database_name="pytest")
    test_collection = db.test
    test_collection.drop()
    write_pickle_to_mongo(proc_path=PROC_DATA_PATH, mongo_collection=test_collection)

    sent = """εἰ μὲν περὶ ἄλλου τινὸς ἢ τοῦ σώματος , ὦ ἄνδρες δικασταί , Καλλίας ἠγωνίζετο , ἐξήρκει ἄν μοι καὶ τὰ παρὰ τῶν ἄλλων εἰρημένα ·"""
    assert gen_sent(test_collection, "43136bd5b0bba2b1a7d9b7301f166bca") == sent
    assert gen_sent(test_collection, "43136bd5b0bba2b1a7d9b7301f166ba") == None

    test_collection.drop()
