import os
import re
import json
import faiss
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from datetime import datetime

# === CONFIG ===
DATA_DIR = "./data/clauses"          # ✅ Adjusted path to current structure
INDEX_DIR = "./data/faiss_index"
CHUNK_SIZE = 500
EMBED_MODEL = "all-MiniLM-L6-v2"

# === SETUP ===
os.makedirs(INDEX_DIR, exist_ok=True)
model = SentenceTransformer(EMBED_MODEL)
index = faiss.IndexFlatL2(384)

clause_db = []
vectors = []

def chunk_text(text, size):
    chunks = []
    current = ""
    for line in text.split('\n'):
        if len(current) + len(line) < size:
            current += line + "\n"
        else:
            chunks.append(current.strip())
            current = line + "\n"
    if current.strip():
        chunks.append(current.strip())
    return chunks

# === INDEXING LOOP ===
doc_id = 0
for filename in tqdm(os.listdir(DATA_DIR), desc="🔍 Indexing clauses"):
    if not filename.endswith(".txt"):
        continue
    file_path = os.path.join(DATA_DIR, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
        if not text:
            print(f"⚠️ Skipping empty file: {filename}")
            continue

    chunks = chunk_text(text, CHUNK_SIZE)
    if not chunks:
        print(f"⚠️ No valid chunks in: {filename}")
        continue

    embeddings = model.encode(chunks, convert_to_numpy=True)  # ✅ Explicit numpy array

    for chunk, embed in zip(chunks, embeddings):
        clause_db.append({
            "id": f"{doc_id}_{filename}",
            "text": chunk
        })
        vectors.append(embed)
    doc_id += 1

# === FINAL STEP ===
if vectors:
    vectors_np = np.array(vectors).astype('float32')
    index.add(vectors_np)

    faiss.write_index(index, os.path.join(INDEX_DIR, "clause_index.faiss"))
    with open(os.path.join(INDEX_DIR, "clause_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(clause_db, f, indent=2)

    print(f"\n✅ Indexed {len(clause_db)} clauses from {doc_id} documents.")
    print(f"📦 FAISS index shape: {vectors_np.shape}")
else:
    print("❌ No valid clauses found. Index not saved.")
