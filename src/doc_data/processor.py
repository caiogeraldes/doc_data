import time
import stanza
import json
from cltk.alphabet.grc import normalize_grc, beta_to_unicode

NLP = stanza.Pipeline(
    lang="grc", package="perseus", verbose=False, depparse_batch_size=400
)


def gen_data(diorisis_file, out_name):
    start = time.time()
    with open(diorisis_file, "r") as file:
        doc = json.load(file)
        texto_beta = ""
        for sent in doc["sentences"]:
            for token in sent["tokens"]:
                texto_beta += token["form"] + " "
        conv = beta_to_unicode.BetaCodeReplacer()
        texto_uni = normalize_grc(conv.replace_beta_code(texto_beta))
        del conv
        del doc
        del texto_beta
        print(f"Processando {diorisis_file}, com {len(texto_uni)} caracteres")

    doc = NLP(texto_uni)
    serialized_string = doc.to_serialized() # type: ignore

    with open(out_name, "wb") as out_file:
        out_file.write(serialized_string)
    end = time.time()
    print("Tempo decorrido: ", end - start)


def read_data(serialized_path):
    with open(serialized_path, "rb") as file:
        pic = file.read()
    doc = stanza.Document.from_serialized(pic)
    return doc


if __name__ == "__main__":
    import os

    from doc_data.main import DIORISIS_PATH, PROC_DATA_PATH

    for document in os.listdir(DIORISIS_PATH):
        if document == "corpus.json":
            continue
        if document.replace("json", "pickle") in os.listdir(PROC_DATA_PATH):
            continue
        else:
            diorisis_file = os.path.join(DIORISIS_PATH, document) # type: ignore
            out_name = os.path.join(PROC_DATA_PATH, document.replace("json", "pickle")) # type: ignore

        gen_data(diorisis_file, out_name)
