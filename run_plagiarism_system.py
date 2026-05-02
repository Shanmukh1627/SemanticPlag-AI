import os
import PyPDF2
import nltk
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

# Load the transformer model (The heart of Semantic Analysis)
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text(file):
    """Extracts text from a PDF or TXT file safely."""
    text = ""
    try:
        # 1. If the user uploads a plain text file (.txt)
        if file.lower().endswith('.txt'):
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()
                
        # 2. If the user uploads a PDF file (.pdf)
        else:
            with open(file, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + " "
                        
    except Exception as e:
        print(f"⚠️ Error reading {file}: {e}")
        
    return text

def generate_report(input_file, matched_file, percentage, ptype):
    """Generates a simple text-based report for the scan."""
    now = datetime.now()
    report = f"""
AI-Based Academic Plagiarism and Idea Similarity Detection System
===============================================================
Date: {now.strftime("%d %B %Y")}
Student File: {input_file}
Matched File: {matched_file}
Plagiarism Percentage: {round(percentage,2)} %
Type: {ptype}
"""
    with open("final_report.txt", "w") as f:
        f.write(report)
    print("\nFinal Report Generated")

def run_system(input_file):
    """The main AI Engine that compares the uploaded file against the cached dataset."""
    
    # 1. Load the pre-computed embeddings (The Cache)
    # If this file doesn't exist, you MUST run 'create_embeddings.py' first!
    try:
        with open("dataset_embeddings.pkl", "rb") as f:
            dataset_cache = pickle.load(f)
    except FileNotFoundError:
        return {"error": "Dataset cache missing. Please run create_embeddings.py first."}

    # 2. Extract and encode the UPLOADED student file
    input_text = extract_text(input_file)
    input_embedding = model.encode(input_text)

    best_score = 0
    best_file = "None"

    # 3. OPTIMIZED COMPARISON: 
    # Instead of reading 1,000 PDFs, we just compare math lists (vectors)
    for filename, cached_embedding in dataset_cache.items():
        score = cosine_similarity(
            [input_embedding],
            [cached_embedding]
        )[0][0]
        
        if score > best_score:
            best_score = score
            best_file = filename

    percentage = float(round(best_score * 100, 2))

    # 4. Categorize the Plagiarism Type
    if percentage >= 90:
        ptype = "Exact Plagiarism"
    elif percentage >= 75:
        ptype = "Paraphrased Plagiarism"
    elif percentage >= 50:
        ptype = "Idea Level Similarity"
    else:
        ptype = "Original Content"

    # 5. Output and logging
    print("\nBest Match File:", best_file)
    print("Plagiarism Percentage:", percentage, "%")
    print("Type:", ptype)

    generate_report(input_file, best_file, percentage, ptype)
    
    return {
        "score": percentage,
        "matched_file": best_file,
        "status": ptype
    }

if __name__ == "__main__":
    # Test run (requires dataset_embeddings.pkl to exist)
    print(run_system("doc1.pdf"))