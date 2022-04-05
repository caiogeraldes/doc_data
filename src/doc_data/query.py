"""
Handles the querying for building the sentences database
"""
import logging
from typing import Optional, Union, Tuple
from pymongo.collection import Collection

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
) -> Collection:
    """
    Takes a collection of tokens built by doc_data.db.write_mongo,
    queries for the proper value for the feature.
    """

    relation, name = validate(feature, value, relation, name)

    collection.aggregate(
        [{"$match": {feature: {relation: value}}}, {"$out": f"{name}"}]
    )

    nhits = len(list(collection.aggregate([{"$match": {feature: {relation: value}}}])))
    print(f"Hits for {feature} = {value}: {nhits}")
    return collection.database[name]


def dependent_query(
    collection: Collection,
    head_collection: Collection,
    feature: str,
    value: Union[str, list[str]],
    relation: str = "$eq",
    name: Optional[str] = None,
):
    print(head_collection)

    relation, name = validate(feature, value, relation, name)

    collection.aggregate(
        [{"$match": {feature: {relation: value}}}, {"$out": f"{name}"}]
    )

    nhits = len(list(collection.aggregate([{"$match": {feature: {relation: value}}}])))
    print(f"Hits for {feature} = {value}: {nhits}")
    return collection.database[name]


if __name__ == "__main__":
    import pandas as pd
    from doc_data.main import MONGO
    from doc_data.db import mongo

    mvi: pd.DataFrame = pd.read_csv("data/mvi.csv")
    lemmata = list(mvi.lemma)
    db = mongo(MONGO)
    token_collection = db.tokens
    main_collection = independent_query(
        token_collection,
        feature="lemma",
        relation="$in",
        value=lemmata,
        name="mviquery",
    )
