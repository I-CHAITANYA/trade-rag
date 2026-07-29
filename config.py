#config.py

import os

from dotenv import load_dotenv


# Load environment variables
load_dotenv()



# =========================
# API Configuration
# =========================

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
).strip()

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "local"
).lower()


# =========================
# Project Paths
# =========================

DATA_PATH = "data"

VECTORSTORE_PATH = (
    "vectorstore/faiss_index"
)



# =========================
# Embedding Configuration
# =========================

EMBEDDING_MODEL = (
    "BAAI/bge-small-en-v1.5"
)



# =========================
# LLM Configuration
# =========================

LLM_MODEL = (
    "gpt-4.1-mini"
)



# =========================
# Text Processing
# =========================

CHUNK_SIZE = 500

CHUNK_OVERLAP = 100



# =========================
# Retrieval
# =========================

TOP_K_RESULTS = 3