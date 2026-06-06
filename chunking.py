import os
import re
import random

RAW_FOLDER = "data/raw"
OUTPUT_FOLDER = "data/processed"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

all_chunks = []  # IMPORTANT: collect everything


def clean_text(text):
    text = re.sub(r"<.*?>", "", text)  # remove HTML
    text = text.replace("&nbsp;", " ")
    text = text.replace("&amp;", "&")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text, chunk_size=400, overlap=75):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if len(chunk.strip()) > 0:
            chunks.append(chunk.strip())

        start = end - overlap

    return chunks


for filename in os.listdir(RAW_FOLDER):
    if filename.endswith(".txt"):
        path = os.path.join(RAW_FOLDER, filename)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        cleaned = clean_text(text)
        chunks = chunk_text(cleaned, 400, 75)

        all_chunks.extend(chunks)  # IMPORTANT FIX

        output_file = os.path.join(
            OUTPUT_FOLDER,
            filename.replace(".txt", "_chunks.txt")
        )

        with open(output_file, "w", encoding="utf-8") as f:
            for i, chunk in enumerate(chunks):
                f.write(f"CHUNK {i+1}\n")
                f.write(chunk + "\n\n")


# =========================
# CHECKPOINT (Milestone 3)
# =========================

print("\n=== CHECKPOINT ===")
print("Total chunks:", len(all_chunks))

print("\nSample chunks:")
for _ in range(5):
    if all_chunks:
        print("----")
        print(random.choice(all_chunks))

print("\nChunking complete.")