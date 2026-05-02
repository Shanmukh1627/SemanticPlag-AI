import PyPDF2
import nltk
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer('all-MiniLM-L6-v2')


def extract_text(file):

    text = ""

    with open(file, "rb") as f:

        reader = PyPDF2.PdfReader(f)

        for page in reader.pages:

            text += page.extract_text()

    return text


def split_sentences(text):

    return nltk.sent_tokenize(text)


def highlight(input_file, dataset_file):

    text1 = extract_text(input_file)

    text2 = extract_text(dataset_file)


    sentences1 = split_sentences(text1)

    sentences2 = split_sentences(text2)


    print("\nMatched Sentences:\n")


    found = False


    for s1 in sentences1:

        for s2 in sentences2:

            emb1 = model.encode(s1)

            emb2 = model.encode(s2)

            score = cosine_similarity([emb1], [emb2])[0][0]


            if score > 0.60:   # lowered threshold

                found = True

                print("Student:", s1)

                print("Dataset:", s2)

                print("Similarity:", round(score*100,2), "%")

                print("------------------")


    if not found:

        print("No matching sentences found above threshold.")



highlight("doc1.pdf", "dataset/paraphrased1.pdf")
