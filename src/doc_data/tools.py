"""
Helper functions
"""
from typing import Union
from pymongo.collection import Collection  # type: ignore


def gen_sent(
    collection: Collection, ts: str  # pylint: disable=invalid-name
) -> Union[str, None]:
    """
    Generates a readable sentence from a text-sentence id (ts) present
    in the collection.
    """
    sent_docs = collection.aggregate(
        [{"$match": {"ts": ts}}, {"$project": {"text": 1}}]
    )

    sent_tokens = [x["text"] for x in sent_docs]
    if len(sent_tokens) == 0:
        return None

    return " ".join(sent_tokens)


if __name__ == "__main__":
    from doc_data.db import mongo
    from doc_data.main import MONGO

    db = mongo(MONGO)
    sent_collection = db.interest_tokens

    print(gen_sent(sent_collection, "229ed0100155655deed043002aa3dbdd"))