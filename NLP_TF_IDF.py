#%%
import glob
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

base_document = "This is an example sentence for the document to be compared"
documents = ["This is the collection of documents to be compared against the base_document"]

def load_documents(directory):
    files = glob.glob(directory + "/*.json")
    print("Located files:", files)
    first_file = files[0]
    other_files = files[1:]
    return first_file, other_files


def process_tfidf_similarity(document):
    base_document, documents = load_documents(document)
    vectorizer = TfidfVectorizer(input="content")

    # To make uniformed vectors, both documents need to be combined first.
    documents.insert(0, base_document)
    document_texts = []
    for document in documents:
        with open(document) as f:
            document_texts.append(json.load(f)["text"])
    embeddings = vectorizer.fit_transform(document_texts)

    cosine_similarities = cosine_similarity(embeddings[0:1], embeddings[1:]).flatten()

    highest_score = 0
    highest_score_index = 0
    for i, score in enumerate(cosine_similarities):
        print(score)
        if highest_score < score:
            highest_score = score
            highest_score_index = i


    most_similar_document = documents[highest_score_index]

    print("Most similar document by TF-IDF with the score:",  highest_score)#, most_similar_document)


for dir in glob.glob("/Users/polly.mckim/Desktop/NewsArticles/*"):
    print("Looking into {}".format(dir))
    process_tfidf_similarity(dir)

#%%