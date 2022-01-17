import stanza


def get_by_lemma(
    doc: stanza.Document,
    lemma,
    filtered_sents=False,
    target_heads=False,
    secondary_filter=False,
):
    hits_sent_id = []
    hits_ids = []

    for sent_id, sent in enumerate(doc.sentences):
        if type(filtered_sents) == list:
            if secondary_filter:
                if sent_id not in secondary_filter:
                    continue
            if sent_id not in filtered_sents:
                continue
        hits_id = []
        for word in sent.words:
            if target_heads:
                if word.head not in target_heads[filtered_sents.index(sent_id)]:
                    continue
            if word.lemma == lemma:
                hits_id.append(word.id)
        if len(hits_id) > 0:
            hits_ids.append(hits_id)
            hits_sent_id.append(sent_id)
    return hits_sent_id, hits_ids


def get_by_morpho(
    doc: stanza.Document,
    morpho,
    filtered_sents=False,
    target_heads=False,
    secondary_filter=False,
):
    hits_sent_id = []
    hits_ids = []

    for sent_id, sent in enumerate(doc.sentences):
        if type(filtered_sents) == list:
            if secondary_filter:
                if sent_id not in secondary_filter:
                    continue
            if sent_id not in filtered_sents:
                continue
        hits_id = []
        for word in sent.words:
            if target_heads:
                if word.head not in list(target_heads[filtered_sents.index(sent_id)]):
                    continue
            if word.upos in ["NOUN", "ADJ", "PRON", "VERB"] and word.feats is not None:
                if morpho in word.feats:
                    hits_id.append(word.id)
        if len(hits_id) > 0:
            hits_ids.append(hits_id)
            hits_sent_id.append(sent_id)
    return hits_sent_id, hits_ids


class FilterRule:
    def __init__(
        self,
        string,
        method,
        filtered_sents=False,
        target_heads=False,
        secondary_filter=False,
    ):
        self.string = string
        self.method = method
        self.filtered_sents = filtered_sents
        self.target_heads = target_heads
        self.secondary_filter = secondary_filter
        self.algorithm = self._filter()

    def _filter(self):
        if self.method == "lemma":
            return get_by_lemma
        elif self.method == "morpho":
            return get_by_morpho
        else:
            return print

    def apply(self, document: stanza.Document):
        return self.algorithm(
            document,
            self.string,
            self.filtered_sents,
            self.target_heads,
            self.secondary_filter,
        )


class FilterPipe:
    def __init__(self, doc: stanza.Document, *filter_rules):
        self.doc = doc
        self.filter_rules = filter_rules
        self.filters = [
            self.build_filter(fil) for fil, _ in enumerate(self.filter_rules)
        ]
        self.result = self.filters[-1].apply(self.doc)[0]  # type: ignore

    def build_filter(self, i):
        fil = self.filter_rules[i]
        if type(fil["filtered_sents"]) != list and not (fil["filtered_sents"] is False):
            fil["filtered_sents"] = self.build_filter(fil["filtered_sents"]).apply(
                self.doc
            )[0]
        if type(fil["target_heads"]) != list and not (fil["target_heads"] is False):
            fil["target_heads"] = self.build_filter(fil["target_heads"]).apply(
                self.doc
            )[1]
        if type(fil["secondary_filter"]) != list and not (
            fil["secondary_filter"] is False
        ):
            fil["secondary_filter"] = self.build_filter(fil["secondary_filter"]).apply(
                self.doc
            )[0]
        return FilterRule(**fil)


if __name__ == "__main__":
    import os
    from doc_data.processor import read_data
    from doc_data.main import PROC_DATA_PATH

    proc_file = "Herodotus (0016) - Histories (001).pickle"
    doc = read_data(os.path.join(PROC_DATA_PATH, proc_file))  # type: ignore
    b = FilterPipe(
        doc,
        {
            "string": "δέομαι",
            "method": "lemma",
            "filtered_sents": False,
            "target_heads": False,
            "secondary_filter": False,
        },
        {
            "string": "Inf",
            "method": "morpho",
            "filtered_sents": 0,
            "target_heads": False,
            "secondary_filter": False,
        },
        {
            "string": "Gen",
            "method": "morpho",
            "filtered_sents": 0,
            "target_heads": 0,
            "secondary_filter": 1,
        },
    )
    for x in b.result:
        print(doc.sentences[x].text)
