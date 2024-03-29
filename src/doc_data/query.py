"""
Handles the querying for building the sentences database
"""
import logging
from typing import Optional, Union, Tuple, List
from pymongo.collection import Collection  # pylint: disable=import-error

logging.basicConfig(level=logging.WARN)


def validate(
    feature: str, value: Union[str, List[str]], relation: str, name: Optional[str]
) -> Tuple[str, str]:
    """
    Validates the set of feature, value, relation and name passed
    to a querying function. Might modify the values for relation
    and name if necessary.
    """
    if isinstance(value, list):
        if relation != "$in":
            logging.warning("Value passed as list, using relation = '$in'")
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
    value: Union[str, List[str]],
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
                {
                    "$project": {
                        "text-sentence": 1,
                        "text-sentence-id": 1,
                        "text-sentence-head": 1,
                    }
                },
            ]
        )
    )

    text_sentence_ids = {x["text-sentence"] for x in hits}

    collection.aggregate(
        [
            {"$match": {"text-sentence": {"$in": list(text_sentence_ids)}}},
            {"$out": "interest_tokens"},
        ]
    )
    collection.aggregate(
        [
            {"$match": {feature: {relation: value}}},
            {
                "$project": {
                    "text-sentence": 1,
                    "text-sentence-id": 1,
                    "text-sentence-head": 1,
                }
            },
            {"$out": name},
        ]
    )

    print(f"Hits for {feature} = {value}: {len(hits)}")
    return collection.database["interest_tokens"], collection.database[name]


def dependent_query(
    collection: Collection,
    feature: str,
    value: str,
    name: str,
    relation: str,
    head_collection: Collection,
):  # pylint: disable=too-many-arguments # pragma: no cover
    """
    TODO
    """
    head_ids = head_collection.distinct("text-sentence-id")
    hits = list(
        collection.aggregate(
            [
                {
                    "$match": {
                        "text-sentence-head": {"$in": head_ids},
                        feature: {relation: value},
                    }
                }
            ]
        )
    )
    text_sentence_ids = {x["text-sentence"] for x in hits}
    collection.aggregate(
        [
            {"$match": {"text-sentence": {"$in": list(text_sentence_ids)}}},
            {"$out": "interest_tokens"},
        ]
    )
    collection.aggregate(
        [
            {
                "$match": {
                    "text-sentence-head": {"$in": head_ids},
                    feature: {relation: value},
                }
            },
            {"$out": name},
        ]
    )

    print(f"Hits for {feature} = {value}: {len(hits)}")
    return collection.database["interest_tokens"], collection.database[name]


def get_value_by_tsi(collection: Collection, text_sentence_id: str) -> List:
    """
    Return a list including a document fetch by to its unique text-sentence-id (tsi).
    """
    hits = collection.aggregate([{"$match": {"text-sentence-id": text_sentence_id}}])

    return list(hits)


def get_dependents_by_tsi(collection: Collection, text_sentence_id: str) -> List:
    """
    Returns a list of documents whose head is marked by a given text-sentence-id (tsi).
    """
    hits = collection.aggregate([{"$match": {"text-sentence-head": text_sentence_id}}])

    return list(hits)
