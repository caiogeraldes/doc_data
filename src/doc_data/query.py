"""
Handles the querying for building the sentences database
"""
import logging
from typing import Optional, Union, Tuple
from pymongo.collection import Collection  # type: ignore

logging.basicConfig(level=logging.WARN)


def validate(
    feature: str, value: Union[str, list[str]], relation: str, name: Optional[str]
) -> Tuple[str, str]:
    """
    Validates the set of feature, value, relation and name passed
    to a querying function. Might modify the values for relation
    and name if necessary.
    """
    if isinstance(value, list):
        logging.warning("Value passed as list, using relation = '$in'")
        if relation != "$in":
            relation = "$in"
        if not name:
            logging.warning(
                "No name passed, the query will be stored as {feature}:list"
            )
            name = f"{feature}:list"
    else:
        if not name:
            logging.warning(
                "No name passed, the query will be stored as {feature}:{value}"
            )
            name = f"{feature}:{value}"
    return relation, name


def independent_query(
    collection: Collection,
    feature: str,
    value: Union[str, list[str]],
    relation: str = "$eq",
    name: Optional[str] = None,
) -> Tuple[Collection, Collection]:
    """
    Takes a collection of tokens built by doc_data.db.write_mongo,
    queries for the proper value for the feature.
    """

    relation, name = validate(feature, value, relation, name)

    hits = list(
        collection.aggregate(
            [
                {"$match": {feature: {relation: value}}},
                {"$project": {"ts": 1, "tsi": 1, "tsh": 1}},
            ]
        )
    )

    ts_ids = {x["ts"] for x in hits}

    collection.aggregate([{"$match": {"ts": {"$in": list(ts_ids)}}}, {"$out": name}])
    collection.aggregate(
        [
            {"$match": {feature: {relation: value}}},
            {"$project": {"ts": 1, "tsi": 1, "tsh": 1}},
            {"$out": name + ":hits"},
        ]
    )

    print(f"Hits for {feature} = {value}: {len(hits)}")
    return collection.database[name], collection.database[name + ":hits"]


def dependent_query(collection, feature, value, name, relation, head_collection):
    """
    TODO
    """
    interest_heads = head_collection.distinct("tsi")

    a = collection.aggregate([
        {"$match": {
            "tsh": {"$in": interest_heads},
            feature: {relation: value}
        }}
    ])
    print(len(list(a)))


if __name__ == "__main__":
    import pandas as pd
    from doc_data.main import MONGO
    from doc_data.db import mongo

    mvi: pd.DataFrame = pd.read_csv("data/mvi.csv")
    lemmata = list(mvi.lemma)
    db = mongo(MONGO)
    token_collection = db.tokens
    sent_collection, hits_collection = independent_query(
        token_collection,
        feature="lemma",
        relation="$in",
        value=lemmata,
        name="mviquery",
    )
    dependent_query(
        token_collection,
        feature="feats",
        relation="$regex",
        value="VerbForm=Inf",
        name="infquery",
        head_collection=hits_collection)
