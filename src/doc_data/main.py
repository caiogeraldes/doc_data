import os
from dotenv import load_dotenv

load_dotenv()

DIORISIS_PATH = os.getenv("DIORISIS_PATH")
PROC_DATA_PATH = os.getenv("PROC_DATA_PATH")
assert DIORISIS_PATH is not None, "Path para DIORISIS não especificada"
assert PROC_DATA_PATH is not None
