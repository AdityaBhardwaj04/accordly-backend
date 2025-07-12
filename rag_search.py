import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths
INDEX_DIR = "../data/faiss_index"
EMBED_MODEL = "all-MiniLM-L6-v2"

# Load index + metadata
index = faiss.read_index(os.path.join(INDEX_DIR, "clause_index.faiss"))
with open(os.path.join(INDEX_DIR, "clause_metadata.json"), "r", encoding="utf-8") as f:
    clause_db = json.load(f)

# Load embedding model
model = SentenceTransformer(EMBED_MODEL)

def retrieve_relevant_clauses(query: str, top_k: int = 5):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), top_k)

    results = []
    for i in I[0]:
        results.append(clause_db[i]["text"])

    return results


if __name__ == "__main__":
    query = "confidential exchange of AI model architecture"
    top_clauses = retrieve_relevant_clauses(query)

    print("Top Relevant Clauses:\n")
    for idx, clause in enumerate(top_clauses, 1):
        print(f"{idx}. {clause}\n")
