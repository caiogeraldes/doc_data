import os
import pytest
from doc_data.db import mongo, write_pickle_to_mongo
from doc_data.query import validate, independent_query, get_value_by_tsi, get_dependents_by_tsi

pytest_plugins = "pytester"

MONGO = "mongodb://localhost:27017"


def test_validation():
    relation, name = validate("a", "a", "$eq", None)
    assert relation == "$eq"
    assert name == "a:a"
    relation, name = validate("a", "a", "$eq", "a")
    assert relation == "$eq"
    assert name == "a"
    relation, name = validate("a", ["a"], "$eq", None)
    assert relation == "$in"
    assert name == "a:list"
    relation, name = validate("a", ["a"], "$in", None)
    assert relation == "$in"
    assert name == "a:list"
    relation, name = validate("a", ["a"], "$in", "a")
    assert relation == "$in"
    assert name == "a"


FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR))
def test_independent_query(datafiles):
    proc_data_path = str(datafiles)
    db = mongo(MONGO, database_name="pytest")
    test_collection = db.test
    test_collection.drop()
    write_pickle_to_mongo(proc_path=proc_data_path, mongo_collection=test_collection)

    out_collection, hit_collection = independent_query(
        test_collection,
        feature="lemma",
        relation="$in",
        value=["δοκέω"],
        name="mviquery",
    )
    text_sentence = [
        "b249b4ddc0d76af602e9747952840b23",
        "ed4ebc8fa7bb495bbb394180d22e52fa",
    ]
    assert out_collection.distinct("text-sentence") == text_sentence
    assert len(out_collection.distinct("_id")) == 95
    assert hit_collection.distinct("text-sentence") == text_sentence
    assert len(hit_collection.distinct("_id")) == len(text_sentence)

    out_collection.drop()
    hit_collection.drop()
    test_collection.drop()


# noinspection SpellCheckingInspection
@pytest.mark.datafiles(os.path.join(FIXTURE_DIR))
def test_get_functions(datafiles):
    proc_data_path = str(datafiles)
    db = mongo(MONGO, database_name="pytest")
    test_collection = db.test
    test_collection.drop()
    write_pickle_to_mongo(proc_path=proc_data_path, mongo_collection=test_collection)

    hits = get_value_by_tsi(
        test_collection, text_sentence_id="75ac92a10ae40756c70da937843aa6d9"
    )

    assert len(hits) == 1
    hit = hits[0]
    assert hit["lemma"] == "εἰ"

    # noinspection SpellCheckingInspection
    hits = get_dependents_by_tsi(
        test_collection, text_sentence_id="a99d9d25a2169f8ca3e87b6c3dccebfd"
    )

    assert len(hits) == 4
    hit = hits[1]
    assert hit["upos"] == "INTJ"
