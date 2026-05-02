from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load pretrained semantic model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Example sentences
text1 = "AI helps students learn faster"
text2 = "Artificial intelligence helps learners study quickly"


# Convert sentences into embeddings
embedding1 = model.encode(text1)
embedding2 = model.encode(text2)

# Calculate cosine similarity
similarity = cosine_similarity([embedding1], [embedding2])

# Print result
print("Similarity Score:", similarity[0][0])

# Classification
score = similarity[0][0]

if score > 0.90:
    print("Type: Exact Plagiarism")
elif score > 0.75:
    print("Type: Paraphrased Plagiarism")
elif score > 0.50:
    print("Type: Idea-Level Similarity")
else:
    print("Type: Original Content")
