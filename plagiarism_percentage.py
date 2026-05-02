from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import spacy

model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = spacy.load("en_core_web_sm")

def extract_text(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()
    return text

def split_sentences(text):
    doc = nlp(text)
    return [sent.text for sent in doc.sents]

text1 = extract_text("doc1.pdf")
text2 = extract_text("doc2.pdf")

sentences1 = split_sentences(text1)
sentences2 = split_sentences(text2)

total = len(sentences1)
matched = 0

for s1 in sentences1:
    for s2 in sentences2:

        emb1 = model.encode(s1)
        emb2 = model.encode(s2)

        score = cosine_similarity([emb1], [emb2])[0][0]

        if score > 0.75:

            matched += 1
            break


percentage = (matched / total) * 100

print("\nPlagiarism Percentage:", round(percentage,2), "%")
# Classification
if percentage > 90:
    ptype = "Exact Plagiarism"
elif percentage > 75:
    ptype = "Paraphrased Plagiarism"
elif percentage > 50:
    ptype = "Idea-Level Similarity"
else:
    ptype = "Original Content"

print("Type:", ptype)
#report saving
from datetime import datetime

now = datetime.now()

report = f"""
AI-Based Academic Plagiarism and Idea Similarity Detection System
==================================================================

Report Generated On: {now.strftime("%d %B %Y")}

--------------------------------------------------

INPUT DETAILS

Student Submitted File: doc1.pdf
Compared With File: doc2.pdf

--------------------------------------------------

RESULT SUMMARY

Plagiarism Percentage: {round(percentage,2)} %

Plagiarism Type: {ptype}

--------------------------------------------------

Technology Used:

- NLP
- BERT Model
- Cosine Similarity


--------------------------------------------------
"""

with open("report.txt", "w", encoding="utf-8") as f:

    f.write(report)

print("Report saved successfully")

