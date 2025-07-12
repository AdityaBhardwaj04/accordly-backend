import os
import faiss
import json
from sentence_transformers import SentenceTransformer

# === CONFIG ===
INDEX_PATH = "./data/faiss_index/clause_index.faiss"
METADATA_PATH = "./data/faiss_index/clause_metadata.json"
EMBED_MODEL = "all-MiniLM-L6-v2"

# === LOAD MODEL AND INDEX ===
model = SentenceTransformer(EMBED_MODEL)
index = faiss.read_index(INDEX_PATH)

# === LOAD METADATA ===
with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# === RAG CLAUSE RETRIEVER ===
def retrieve_relevant_clauses(query: str, top_k: int = 5):
    embedding = model.encode([query])
    scores, indices = index.search(embedding, top_k)

    results = []
    for idx in indices[0]:
        if 0 <= idx < len(metadata):
            results.append(metadata[idx])
    return results
