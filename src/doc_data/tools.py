"""
Helper functions
"""
from typing import Union, List
from pymongo.collection import Collection


def gen_sent(
    collection: Collection, text_sentence: str  # pylint: disable=invalid-name
) -> Union[str, None]:
    """
    Generates a readable sentence from a text-sentence id (text_sentence) present
    in the collection.
    """
    sent_docs = collection.aggregate(
        [{"$match": {"text-sentence": text_sentence}}, {"$project": {"text": 1}}]
    )

    sent_tokens = [x["text"] for x in sent_docs]
    if len(sent_tokens) == 0:
        return None

    return " ".join(sent_tokens)


def gen_meta(collection: Collection, text_sentence: str) -> Union[str, None]:
    """
    TODO
    """
    sample_token = collection.find_one({"text-sentence": text_sentence})
    if sample_token is None:
        return None
    author = sample_token["author"]
    doc_name = sample_token["doc_name"]
    return f"{author} - {doc_name}"


def gen_hits(
    main_collection: Collection, text_sentence: str, hit_collections: List[Collection]
):
    """
    TODO
    """

    data = {}
    tokens = list(main_collection.find({"text-sentence": text_sentence}))
    for hit_collection in hit_collections:
        data[hit_collection.name] = [
            x["text"] for x in tokens if x["_id"] in hit_collection.distinct("_id")
        ]

    return data


if __name__ == "__main__":  # pragma: no cover
    from doc_data.db import mongo
    from doc_data.main import MONGO

    db = mongo(MONGO)
    sent_collection = db.interest_tokens

    print(gen_sent(sent_collection, "229ed0100155655deed043002aa3dbdd"))
