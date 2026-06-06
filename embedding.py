import os
import chromadb
from sentence_transformers import SentenceTransformer

PROCESSED_FOLDER = "data/processed"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create Chroma DB client (in-memory for now)
client = chromadb.Client()
collection = client.create_collection(name="cs_unofficial_guide")


def load_chunks():
    chunks = []

    for filename in os.listdir(PROCESSED_FOLDER):
        if filename.endswith("_chunks.txt"):
            path = os.path.join(PROCESSED_FOLDER, filename)

            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            current_chunk = ""
            chunk_id = 0

            for line in lines:
                if line.startswith("CHUNK"):
                    if current_chunk.strip():
                        chunks.append({
                            "text": current_chunk.strip(),
                            "source": filename,
                            "chunk_id": chunk_id
                        })
                        chunk_id += 1
                        current_chunk = ""
                else:
                    current_chunk += line

            # last chunk
            if current_chunk.strip():
                chunks.append({
                    "text": current_chunk.strip(),
                    "source": filename,
                    "chunk_id": chunk_id
                })

    return chunks


print("Loading chunks...")
chunks = load_chunks()

print(f"Total chunks loaded: {len(chunks)}")

print("Embedding chunks...")

for i, chunk in enumerate(chunks):
    embedding = model.encode(chunk["text"]).tolist()

    collection.add(
        documents=[chunk["text"]],
        embeddings=[embedding],
        ids=[f"{chunk['source']}_{chunk['chunk_id']}"],
        metadatas=[{
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"]
        }]
    )

print("Embedding complete!")


# -------------------------
# RETRIEVAL FUNCTION
# -------------------------

def retrieve(query, k=4):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    for i in range(len(results["documents"][0])):
        print("\n--- RESULT", i + 1, "---")
        print("TEXT:", results["documents"][0][i])
        print("SOURCE:", results["metadatas"][0][i])
        print("DISTANCE:", results["distances"][0][i])


# -------------------------
# TEST YOUR SYSTEM
# -------------------------

if __name__ == "__main__":
    print("\nTEST QUERY 1")
    retrieve("How hard is CS140?")

    print("\nTEST QUERY 2")
    retrieve("What is workload like in CS220?")

    print("\nTEST QUERY 3")
    retrieve("Should I take CS140 with CS220?")