from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import spacy

# Load models
model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = spacy.load("en_core_web_sm")

# Extract text
def extract_text(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()
    return text

# Split into sentences
def split_sentences(text):
    doc = nlp(text)
    return [sent.text for sent in doc.sents]

# Load files
text1 = extract_text("doc1.pdf")
text2 = extract_text("doc2.pdf")

sentences1 = split_sentences(text1)
sentences2 = split_sentences(text2)

# Compare sentence by sentence
print("\nPlagiarized Sentences:\n")

for s1 in sentences1:
    for s2 in sentences2:

        emb1 = model.encode(s1)
        emb2 = model.encode(s2)

        score = cosine_similarity([emb1], [emb2])[0][0]

        if score > 0.75:

            print("Sentence 1:", s1)
            print("Sentence 2:", s2)
            print("Similarity:", score)
            print("----------------------")
