import os
import PyPDF2
import pickle
from sentence_transformers import SentenceTransformer

# Load the model once
model = SentenceTransformer('all-MiniLM-L6-v2')
DATASET_FOLDER = "dataset"

def extract_text(file_path):
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
    except Exception as e:
        print(f"Could not read {file_path}: {e}")
    return text

# This dictionary will store { "filename.pdf": [0.12, -0.05, ...] }
dataset_cache = {}

print(f"🚀 Starting pre-computation for {len(os.listdir(DATASET_FOLDER))} files...")

for filename in os.listdir(DATASET_FOLDER):
    if filename.endswith(".pdf"):
        path = os.path.join(DATASET_FOLDER, filename)
        print(f"Processing: {filename}")
        
        text = extract_text(path)
        if text.strip():
            # Create the math representation (embedding)
            embedding = model.encode(text)
            dataset_cache[filename] = embedding

# Save the math to a "Pickle" file (this is your cache)
print("💾 Saving embeddings to dataset_embeddings.pkl...")
with open("dataset_embeddings.pkl", "wb") as f:
    pickle.dump(dataset_cache, f)

print("✅ Success! Your 1,000-document cache is ready.")