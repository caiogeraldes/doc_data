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
from doc_data.main import PROC_DATA_PATH, MONGO


def mongo(mongo_url=MONGO, database_name="phd"):
    """
    Connect to MongoDB
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
    Converts the data in PROC_DATA_PATH to a MongoDB.
    Each token becomes a single MongoDB Document.
    """
    files = os.listdir(proc_path)
    n_files = len(files)
    for f_id, proc_file in enumerate(files):
        author, title = proc_file.replace(".pickle", "").split("-", 1)
        author = author.strip()
        title = title.strip()
        doc_d = read_data(os.path.join(PROC_DATA_PATH, proc_file)).to_dict()  # type: ignore
        # doc_d = doc.to_dict()
        pbar = trange(
            len(doc_d),
            desc=f"Sent. from {author}-{title} ({f_id+1}/{n_files})",
            leave=True,
        )
        for i, j in zip(pbar, doc_d):
            for t_id, token in enumerate(j):
                token["doc_name"] = title
                token["author"] = author
                token["text_id"] = md5(f"{token['author']}-{token['doc_name']}".encode()).hexdigest()
                token["sent_id"] = i + 1
                token["sid_id"] = (token["sent_id"], token["id"])
                token["sid_hid"] = (token["sent_id"], token["head"])
                token["_id"] = md5(
                    f"{token['author']}-{token['doc_name']}-{token['sid_id']}".encode()
                ).hexdigest()
                try:
                    mongo_collection.insert_one(token)
                except DuplicateKeyError as _:
                    del _
                finally:
                    pbar.set_description(
                        f"Sent. from {author}-{title} ({f_id+1}/{n_files},sent:{i},token:{t_id})"
                    )  # add dynamic bar description
                    pbar.refresh()  # to show immediately the update
