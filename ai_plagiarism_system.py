import os
import PyPDF2
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

# Load AI Model
model = SentenceTransformer('all-MiniLM-L6-v2')


# Extract text from PDF
def extract_text(file):

    text = ""

    with open(file, "rb") as f:

        reader = PyPDF2.PdfReader(f)

        for page in reader.pages:

            text += page.extract_text()

    return text


# Compare input with dataset
def compare_with_dataset(input_file):

    dataset_path = "dataset"

    input_text = extract_text(input_file)

    input_embedding = model.encode(input_text)

    best_score = 0

    best_file = ""


    for file in os.listdir(dataset_path):

        file_path = os.path.join(dataset_path, file)

        dataset_text = extract_text(file_path)

        dataset_embedding = model.encode(dataset_text)

        score = cosine_similarity(
            [input_embedding],
            [dataset_embedding]
        )[0][0]


        if score > best_score:

            best_score = score

            best_file = file


    percentage = best_score * 100


    #classification logic (INSIDE function)
    if percentage >= 85:

        ptype = "Exact Plagiarism"

    elif percentage >= 70:

        ptype = "Paraphrased Plagiarism"

    elif percentage >= 50:

        ptype = "Idea Level Similarity"

    else:

        ptype = "Original Content"


    print("\nBest Match File:", best_file)

    print("Plagiarism Percentage:", round(percentage,2), "%")

    print("Type:", ptype)


    generate_report(input_file, best_file, percentage, ptype)



# Generate final report
def generate_report(input_file, matched_file, percentage, ptype):

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

    with open("final_report.txt","w") as f:

        f.write(report)


    print("\nFinal Report Generated")



# Run system
compare_with_dataset("doc1.pdf")
