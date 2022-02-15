"""
Module for processing and generating the data for my PhD
"""
import time
import json
import stanza  # type: ignore
from cltk.alphabet.grc import normalize_grc, beta_to_unicode  # type: ignore

NLP = stanza.Pipeline(
    lang="grc", package="perseus", verbose=False, depparse_batch_size=400
)


def gen_data(diorisis_file, out_name):
    """
    Generates the stanza document and saves it in the format .pickle.
    """
    start = time.time()
    with open(diorisis_file, "r", encoding='utf-8') as file:
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
    serialized_string = doc.to_serialized()  # type: ignore

    with open(out_name, "wb") as out_file:
        out_file.write(serialized_string)
    end = time.time()
    print("Tempo decorrido: ", end - start)


def read_data(serialized_path):
    """
    Reads a stanza document serialized to pickle file.
    """
    with open(serialized_path, "rb") as file:
        pic = file.read()
    doc = stanza.Document.from_serialized(pic)
    return doc
