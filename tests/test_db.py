from pytest import raises
from doc_data.db import mongo, write_pickle_to_mongo
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
PROC_DATA_PATH = "/home/silenus/docs/Academia/Doutorado/data/doc_data/tests/data/proc/"
MONGO_ERROR_PATH = "mongodb+srv://silenus:86432@cluster0.ckrsn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


def test_mongo_connection():
    db = mongo(database_name="test")
    assert(isinstance(db, Database))
    with raises(ConnectionFailure) as excinfo:
        db = mongo(MONGO_ERROR_PATH, database_name="test")
    assert(excinfo.errisinstance(ConnectionFailure))


def test_write_pickle_to_mongo():
    db = mongo(database_name="test")
    test_collection = db.test
    test_collection.drop()
    write_pickle_to_mongo(proc_path=PROC_DATA_PATH, mongo_collection=test_collection)
    write_pickle_to_mongo(proc_path=PROC_DATA_PATH, mongo_collection=test_collection)
    test_collection.drop()
