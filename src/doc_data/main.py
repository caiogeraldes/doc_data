"""
Entry point to generate my PhD data
"""
import os
from dotenv import load_dotenv

load_dotenv()

DIORISIS_PATH = os.getenv("DIORISIS_PATH")
PROC_DATA_PATH = os.getenv("PROC_DATA_PATH")
MONGO = os.getenv("MONGO")
STANZA_RESOURCES_DIR = os.getenv("STANZA_RESOURCES_DIR")
MVI = os.getenv("MVI")
LOG = os.getenv("LOG")
assert DIORISIS_PATH is not None, "Path to DIORISIS unspecified"
assert PROC_DATA_PATH is not None, "Path to serialized stanza.Documents unspecified"
assert MONGO is not None, "MongoDB connection unspecified"
assert STANZA_RESOURCES_DIR is not None, "Path to stanza_resources unspecified"
assert MVI is not None, "Path to mvi.csv unspecified"

if __name__ == "__main__":  # pragma: no cover
    import time
    import logging
    import pandas as pd
    from pymongo.database import Database  # type: ignore
    from pymongo.collection import Collection  # type: ignore
    from tqdm import trange  # type: ignore
    import stanza  # type: ignore
    from doc_data.processor import gen_data
    from doc_data.db import mongo, write_pickle_to_mongo
    from doc_data.query import independent_query, dependent_query

    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(
        filename=LOG,
        format="%(asctime)s - %(message)s",
        filemode="w",
        level=logging.INFO,
    )

    start = time.time()

    if not os.path.exists(PROC_DATA_PATH):
        logging.warning("Creating %s", {PROC_DATA_PATH})
        os.mkdir(PROC_DATA_PATH)

    if not os.path.exists(STANZA_RESOURCES_DIR):
        logging.info("Downloading stanza resources to: %s", STANZA_RESOURCES_DIR)
        stanza.download(lang="grc", package="perseus", model_dir=STANZA_RESOURCES_DIR)
    elif len(os.listdir(STANZA_RESOURCES_DIR)) == 0:
        logging.info("Downloading stanza resources to: %s", STANZA_RESOURCES_DIR)
        stanza.download(lang="grc", package="perseus", model_dir=STANZA_RESOURCES_DIR)

    logging.info("Loading NLP Pipeline")
    nlp = stanza.Pipeline(
        lang="grc",
        package="perseus",
        verbose=False,
        depparse_batch_size=400,
        dir=STANZA_RESOURCES_DIR,
    )

    start_serialization = time.time()

    diorisis_files = [x for x in os.listdir(DIORISIS_PATH) if x != "corpus.json"]
    n_files = len(diorisis_files)
    pbar = trange(n_files, desc="Processing Diorisis data", leave=True)
    for i, json_file in zip(pbar, diorisis_files):
        fpath = os.path.join(DIORISIS_PATH, json_file)
        opath = os.path.join(PROC_DATA_PATH, json_file.replace("json", "pickle"))
        if not os.path.exists(opath):
            STATUS = "New"
            logging.info("Processing file %s", fpath)
            gen_data(nlp, str(fpath), str(opath))
        else:
            STATUS = "Existing"
            logging.warning("File %s already existed in %s", str(opath), PROC_DATA_PATH)
        pbar.set_description(
            f"Processed file {json_file} ({i + 1}/{n_files} - {STATUS})"
        )
        pbar.refresh()

    end = time.time()
    logging.info(
        "stanza.Document serialization took %s seconds", end - start_serialization
    )

    start_mongo = time.time()

    logging.info(
        "Building MongoDB tokens collection from the data in: %s", PROC_DATA_PATH
    )
    db: Database = mongo(MONGO)
    col: Collection = db.tokens
    write_pickle_to_mongo(PROC_DATA_PATH, col)

    end = time.time()
    logging.info("Creation of tokens collection took %s seconds", end - start_mongo)

    start_query = time.time()

    mvi_df: pd.DataFrame = pd.read_csv(MVI)

    lemmata = list(mvi_df.lemma)
    sent_collection, mvi_collection = independent_query(
        col,
        feature="lemma",
        relation="$in",
        value=lemmata,
        name="mviquery",
    )
    sent_collection, mvi_collection = dependent_query(
        sent_collection,
        feature="feats",
        relation="$regex",
        value="VerbForm=Inf",
        name="infquery",
        head_collection=mvi_collection,
    )
    sent_collection, mvi_collection = dependent_query(
        sent_collection,
        feature="feats",
        relation="$regex",
        value="Case=Dat|Case=Gen",
        name="xobjquery",
        head_collection=mvi_collection,
    )

    end = time.time()
    logging.info("Queries on MongoDB took %s seconds", end - start_query)

    end = time.time()
    logging.info("Full database generation took %s seconds", end - start)
