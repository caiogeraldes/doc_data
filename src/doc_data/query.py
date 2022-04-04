"""
Handles the querying for building the sentences database
"""
from pymongo.collection import Collection


def main_query(collection: Collection, feature: str, value: str) -> list:
    """
    Takes a collection of tokens built by doc_data.db.write_mongo,
    queries for the proper value for the feature.
    """
    doc = collection. aggregate([{'$match': { feature: value }}])
    return list(doc)


if __name__ == "__main__":
    import pandas as pd

    from doc_data.main import MONGO
    from doc_data.db import mongo

    mvi: pd.DataFrame = pd.read_csv("~/proj/doc_data/data/mvi.csv")
    mvi.set_index("lemma", inplace=True)


    db = mongo(MONGO)
    tokenCollection = db.tokens
    for i in mvi.index:
        a = main_query(tokenCollection, "lemma", i)
        mvi.loc[[i]]["n"] = len(a)

    print(mvi.n)
