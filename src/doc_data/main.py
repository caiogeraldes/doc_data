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
assert DIORISIS_PATH is not None, "Path para DIORISIS não especificada"
assert PROC_DATA_PATH is not None
assert MONGO is not None
assert STANZA_RESOURCES_DIR is not None

if __name__ == "__main__":  # pragma: no cover
    import os
    import time
    import logging
    from tqdm import trange
    import stanza
    from doc_data.processor import gen_data
    from doc_data.db import mongo, write_pickle_to_mongo

    logging.basicConfig(filename="data.processing.log",
                        format='%(asctime)s - %(message)s',
                        filemode="w",
                        level=logging.INFO)

    start = time.time()

    if not os.path.exists(PROC_DATA_PATH):
        logging.warning(f"Creating {PROC_DATA_PATH}")
        os.mkdir(PROC_DATA_PATH)

    if not os.path.exists(STANZA_RESOURCES_DIR):
        logging.info(f"Downloading stanza resources to: {STANZA_RESOURCES_DIR}")
        stanza.download(lang="grc", package="perseus", model_dir=STANZA_RESOURCES_DIR)
    elif len(os.listdir(STANZA_RESOURCES_DIR)) == 0:
        logging.info(f"Downloading stanza resources to: {STANZA_RESOURCES_DIR}")
        stanza.download(lang="grc", package="perseus", model_dir=STANZA_RESOURCES_DIR)

    logging.info("Loading NLP Pipeline")
    nlp = stanza.Pipeline(
        lang="grc",
        package="perseus",
        verbose=False,
        depparse_batch_size=400,
        dir=STANZA_RESOURCES_DIR,
    )

    start_serializacao = time.time()

    diorisis_files = [x for x in os.listdir(DIORISIS_PATH) if x != "corpus.json"]
    n_files = len(diorisis_files)
    pbar = trange(n_files, desc="Processing Diorisis data", leave=True)
    for i, json_file in zip(pbar, diorisis_files):
        fpath = os.path.join(DIORISIS_PATH, json_file)
        opath = os.path.join(PROC_DATA_PATH, json_file.replace("json", "pickle"))
        if not os.path.exists(opath):
            status = "New"
            logging.info(f"Processing file {fpath}")
            gen_data(nlp, str(fpath), str(opath))
        else:
            status = "Existing"
            logging.warning(f"File {str(opath)} already existed in {PROC_DATA_PATH}")
        pbar.set_description(f"Processed file {json_file} ({i+1}/{n_files} - {status})")
        pbar.refresh()

    end = time.time()
    logging.info(f"Criação de arquivos serializados {end-start_serializacao} segundos")

    start_mongo = time.time()

    logging.info(f"Preparando dados de: {PROC_DATA_PATH}")
    db = mongo(MONGO)
    col = db.tokens
    write_pickle_to_mongo(PROC_DATA_PATH, col)

    end = time.time()
    logging.info(f"Criação do MongoDB demorou {end-start_mongo} segundos")

    end = time.time()
    logging.info(f"Criação do completa do banco de dados demorou {end-start} segundos")
