import os
import PyPDF2
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')


# Extract text
def extract_text(file):

    text = ""

    with open(file, "rb") as f:

        reader = PyPDF2.PdfReader(f)

        for page in reader.pages:

            text += page.extract_text()

    return text



# Compare function
def check_similarity(file1, file2):

    text1 = extract_text(file1)

    text2 = extract_text(file2)

    emb1 = model.encode(text1)

    emb2 = model.encode(text2)

    score = cosine_similarity([emb1], [emb2])[0][0]

    percentage = score * 100

    if percentage >= 50:
        return "Plagiarism"

    else:
        return "Original"



# Dataset ground truth

test_cases = [

("dataset/original1.pdf", "dataset/paraphrased1.pdf", "Plagiarism"),

("dataset/original2.pdf", "dataset/paraphrased2.pdf", "Plagiarism"),

("dataset/original1.pdf", "dataset/different1.pdf", "Original"),

("dataset/original2.pdf", "dataset/different2.pdf", "Original"),

]



correct = 0

total = len(test_cases)



for file1, file2, actual in test_cases:

    predicted = check_similarity(file1, file2)

    print("\nComparing:", file1, "VS", file2)

    print("Actual:", actual)

    print("Predicted:", predicted)


    if predicted == actual:

        correct += 1



accuracy = (correct / total) * 100


print("\n--------------------------------")

print("System Accuracy:", accuracy, "%")

print("--------------------------------")