"""
Module for processing and generating the serialized stanza datase
from .json files of the Diorisis Corpus.
"""
import json
import stanza  # type: ignore
from cltk.alphabet.grc import normalize_grc, beta_to_unicode  # type: ignore


def gen_data(nlp: stanza.Pipeline, diorisis_file: str, out_name: str) -> None:
    """
    Generates the stanza document and saves it in the format .pickle.
    args:
        nlp: [stanza.Pipeline] A `stanza` Pipeline for Greek.
        diorisis_file: [str] .json file from the Diorisis corpus
            (at:[https://figshare.com/articles/dataset/The_Diorisis_Ancient_Greek_Corpus_JSON_/])
        out_name: [str] Name for the output serialized file to be created
            (recommended to use a .pickle format)
    """
    with open(diorisis_file, "r", encoding="utf-8") as file:
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

    doc = nlp(texto_uni)
    serialized_string = doc.to_serialized()  # type: ignore

    with open(out_name, "wb") as out_file:
        out_file.write(serialized_string)


def read_data(serialized_path: str) -> stanza.Document:
    """
    Reads a stanza document serialized to pickle file.
    """
    with open(serialized_path, "rb") as file:
        pic = file.read()
    doc = stanza.Document.from_serialized(pic)
    return doc
