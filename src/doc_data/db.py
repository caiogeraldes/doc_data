"""
Converts the data in PROC_DATA_PATH to a MongoDB.
Each token becomes a single MongoDB Document.
"""
import os
from hashlib import md5
from tqdm import trange  # type: ignore
from pymongo import MongoClient  # type: ignore
from pymongo.errors import ConnectionFailure, DuplicateKeyError  # type: ignore
from doc_data.processor import read_data


def mongo(mongo_url, database_name="phd"):
    """
    Connects to MongoDB
    args:
        mongo_url: [str] URL to estalish a Mongo Connection.
        database_name: [str] Name of the database to host the collections.
    """
    try:
        client = MongoClient(mongo_url)
        print("Connected successfully")
    except:  # noqa: E722  pylint: disable=W0707
        raise ConnectionFailure

    database = client[database_name]
    return database


def write_pickle_to_mongo(proc_path, mongo_collection):
    """
    Converts the serialized stanza data in proc_path to a MongoDB collection.
    Each token becomes a single MongoDB Document.
    args:
        proc_path: [str] path to where the serialized stanza data is stored.
        mongo_collection: [pymongo.collection.Collection] Mongo collection to host the tokens.
    """
    files = [x for x in os.listdir(proc_path) if x.endswith("pickle")]
    n_files = len(files)
    for f_id, proc_file in enumerate(files):
        author, title = proc_file.replace(".pickle", "").split("-", 1)
        author = author.strip()
        title = title.strip()
        doc_d = read_data(os.path.join(proc_path, proc_file)).to_dict()  # type: ignore
        pbar = trange(  # Progress bar
            len(doc_d),
            desc=f"Sent. from {author}-{title} ({f_id+1}/{n_files})",
            leave=True,
        )
        for i, j in zip(pbar, doc_d):
            for t_id, token in enumerate(j):
                # Generates data not accounted for by stanza, including hashed ids
                token["doc_name"] = title
                token["author"] = author
                token["text_id"] = md5(
                    f"{token['author']}-{token['doc_name']}".encode()
                ).hexdigest()
                token["sent_id"] = i + 1
                token["sid_id"] = (token["sent_id"], token["id"])
                token["sid_hid"] = (token["sent_id"], token["head"])
                token["_id"] = md5(
                    f"{token['author']}-{token['doc_name']}-{token['sid_id']}".encode()
                ).hexdigest()
                # Avoids trying to insert the same token twice.
                try:
                    mongo_collection.insert_one(token)
                except DuplicateKeyError as _:
                    del _
                finally:
                    pbar.set_description(
                        f"Sent. from {author}-{title} ({f_id+1}/{n_files},sent:{i},token:{t_id})"
                    )  # add dynamic bar description
                    pbar.refresh()  # to show immediately the update
