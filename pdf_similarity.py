from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2

# Load AI Model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to extract text from PDF
def extract_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Read PDFs
text1 = extract_text("doc1.pdf")
text2 = extract_text("doc2.pdf")

# Convert to embeddings
embedding1 = model.encode(text1)
embedding2 = model.encode(text2)

# Similarity
similarity = cosine_similarity([embedding1], [embedding2])

score = similarity[0][0]

print("Plagiarism Score:", score)

# Classification
if score > 0.90:
    print("Exact Plagiarism")
elif score > 0.75:
    print("Paraphrased Plagiarism")
elif score > 0.60:
    print("Idea-Level Similarity")
else:
    print("Original Content")
