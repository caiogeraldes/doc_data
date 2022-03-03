from typing import List
from doc_data.db import mongo

# Separate by author-text (text_id)

db = mongo()
text_ids: List[str] = db.teste.distrinct("text_id")

# BEGIN SEARCH

## Step 1: select main verbs of interest

mvi: List[str]

