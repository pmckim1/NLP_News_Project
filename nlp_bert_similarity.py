#%%
import glob
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from nltk import sent_tokenize

from sentence_transformers import SentenceTransformer


#%%
base_document = "This is an example sentence for the document to be compared"
documents = ["This is the collection of documents to be compared against the base_document"]

def load_documents(directory):
    files = glob.glob(directory + "/*.json")
    print("Located files:", files)
    first_file = files[0]
    other_files = files[1:]
    return first_file, other_files

def process_bert_similarity(document):
	# This will download and load the pretrained model offered by UKPLab.
	base_document, documents = load_documents(document)
	model = SentenceTransformer('bert-base-nli-mean-tokens')

	# Although it is not explicitly stated in the official document of sentence transformer, the original BERT is meant for a shorter sentence. We will feed the model by sentences instead of the whole documents.
	sentences = sent_tokenize(base_document)
	base_embeddings_sentences = model.encode(sentences)
	base_embeddings = np.mean(np.array(base_embeddings_sentences), axis=0)

	vectors = []
	for i, document in enumerate(documents):

		sentences = sent_tokenize(document)
		embeddings_sentences = model.encode(sentences)
		embeddings = np.mean(np.array(embeddings_sentences), axis=0)

		vectors.append(embeddings)

		print("making vector at index:", i)

	scores = cosine_similarity([base_embeddings], vectors).flatten()

	highest_score = 0
	highest_score_index = 0
	lowest_score = 1
	lowest_score_index = 0
	for i, score in enumerate(scores):
		print(score)
		if highest_score < score:
			highest_score = score
			highest_score_index = i
		if lowest_score > score:
			lowest_score = score
			lowest_score_index = i
	

	most_similar_document = documents[highest_score_index]
	print("Most similar document by BERT with the score:",  highest_score, )#, most_similar_document)
	print("Least similar document by BERT with the score:",  lowest_score, )
for dir in glob.glob("/Users/polly.mckim/Desktop/NewsArticles/*"):
    print("Looking into {}".format(dir))
    process_bert_similarity(dir)

# %%
