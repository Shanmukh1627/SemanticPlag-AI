import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
from datetime import datetime

# Load AI Model
model = SentenceTransformer('all-MiniLM-L6-v2')

dataset_folder = "dataset"

files = os.listdir(dataset_folder)

results = []

# Function to extract text
def extract_text(file_path):

    text = ""

    with open(file_path, 'rb') as file:

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:

            text += page.extract_text()

    return text


# Compare all files
for i in range(len(files)):

    for j in range(i+1, len(files)):

        file1 = files[i]
        file2 = files[j]

        path1 = os.path.join(dataset_folder, file1)
        path2 = os.path.join(dataset_folder, file2)

        text1 = extract_text(path1)
        text2 = extract_text(path2)

        emb1 = model.encode(text1)
        emb2 = model.encode(text2)

        score = cosine_similarity([emb1], [emb2])[0][0]

        percentage = round(score * 100, 2)

        if score > 0.90:
            ptype = "Exact Plagiarism"

        elif score > 0.75:
            ptype = "Paraphrased Plagiarism"

        elif score > 0.60:
            ptype = "Idea Level Similarity"

        else:
            ptype = "Original Content"

        results.append(f"{file1}  VS  {file2}")
        results.append(f"Score: {percentage}%")
        results.append(f"Type: {ptype}")
        results.append("---------------------------------")


# Save report

now = datetime.now()

report = f"""
DATASET PLAGIARISM REPORT
=========================

Generated On: {now.strftime("%d %B %Y")}

---------------------------------

"""

report += "\n".join(results)

with open("dataset_report.txt", "w") as f:

    f.write(report)


print("Dataset Report Generated Successfully")
