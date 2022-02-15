"""
Entry point to generate my PhD data
"""
import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()

DIORISIS_PATH = os.getenv("DIORISIS_PATH")
PROC_DATA_PATH = os.getenv("PROC_DATA_PATH")
MONGO = os.getenv("MONGO")
assert DIORISIS_PATH is not None, "Path para DIORISIS não especificada"
assert PROC_DATA_PATH is not None
assert MONGO is not None
