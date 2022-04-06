import os
import pytest
from pytest import raises
from doc_data.db import mongo, write_pickle_to_mongo
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

pytest_plugins = "pytester"

MONGO = "mongodb+srv://pytest:1234@pytest.ckrsn.mongodb.net/pytest?retryWrites=true&w=majority"
MONGO_ERROR_PATH = "mongodb+srv://silenus:86432@cluster0.ckrsn.mongodb.net/pytest?retryWrites=true&w=majority"


def test_mongo_connection():
    db = mongo(MONGO, database_name="pytest")
    assert isinstance(db, Database)
    with raises(ConnectionFailure) as excinfo:
        mongo(MONGO_ERROR_PATH, database_name="pytest")
    assert excinfo.errisinstance(ConnectionFailure)


FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR))
def test_write_pickle_to_mongo(datafiles):
    proc_data_path = str(datafiles)
    db = mongo(MONGO, database_name="pytest")
    test_collection = db.test
    test_collection.drop()
    write_pickle_to_mongo(proc_path=proc_data_path, mongo_collection=test_collection)
    write_pickle_to_mongo(proc_path=proc_data_path, mongo_collection=test_collection)
    test_collection.drop()
