from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import spacy

nlp = spacy.load('en_core_web_md')

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')


def get_embedding(text):
    """
    Compute the BERT embedding for the given text.

    Args:
        text (str): The input text to be embedded.

    Returns:
        numpy.ndarray: The mean embedding of the input text.
    """
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()[0]


def divide_in_sentences(text):
    """
    Divide the text into sentences and return their positions.

    Args:
        text (str): The input text to be divided into sentences.

    Returns:
        list: A list of tuples containing the sentence text and its start and end positions.
    """
    doc = nlp(text)
    return [(sent.text.strip(), (sent[0].idx, sent[-1].idx + len(sent[-1].text))) for sent in doc.sents]


def compute_similarities(embeddings):
    """
    Compute the cosine similarities between all sentence pairs in the given embeddings.

    Args:
        embeddings (list): A list of lists, where each sublist contains tuples of embeddings and their positions.

    Returns:
        list: A list of tuples, where each tuple contains the indices of two documents, their positions, 
        and the cosine similarity between the sentence embeddings at those positions.
    """
    similarities = []
    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            for seg1, pos1 in embeddings[i]:
                for seg2, pos2 in embeddings[j]:
                    similarity = cosine_similarity([seg1], [seg2])[0][0]
                    similarities.append(((i, pos1), (j, pos2), similarity))
    return similarities


def categorize_similarities(similarities, similarity_floor=0.86, plagiarisim_floor=0.9):
    """
    Categorize the given similarities into plagiarism, theme, and different categories based
    on the similarity thresholds.

    Args:
        similarities (list): A list of tuples, where each tuple contains two indices, two positions,
        and a similarity score.

        similarity_floor (float, optional): The lower threshold for similarity. Defaults to  0.86.

        plagiarism_floor (float, optional): The upper threshold for similarity to consider it as plagiarism.
        Defaults to  0.9.

    Returns:
        tuple: A tuple of three lists, where each list contains the categorized similarities.
        - plagiarism: Similarities that have a similarity score greater than the plagiarism_floor.
        - same_theme: Similarities that have a similarity score greater than the similarity_floor
        but less than or equal to the plagiarism_floor.
        - different: Similarities that have a similarity score less than or equal to the similarity_floor.
    """
    plagiarism = []
    same_theme = []
    different = []
    for similarity in similarities:
        if similarity[2] > similarity_floor:
            if similarity[2] > plagiarisim_floor:
                plagiarism.append(similarity)
            else:
                same_theme.append(similarity)
        else:
            different.append(similarity)
    return plagiarism, same_theme, different


def calculate_embeddings(documents):
    """
    Calculate the embeddings for each sentence in the provided documents.

    Args:
        documents (list): A list of documents, where each document is a string.

    Returns:
        list: A nested list of tuples, where each tuple contains an embedding and its position within the document.
        The outer list represents each document.
    """
    return [[(get_embedding(sentence), pos) for sentence, pos in divide_in_sentences(doc)] for doc in documents]


def detect(documents):
    """
    Detect plagiarism, thematic similarity, and difference in documents.

    Args:
        documents (list): A list of documents to be analyzed.

    Returns:
        tuple: A tuple containing three lists: plagiarism, theme, and different.
        Each list contains tuples of sentence pairs with their similarity scores.
    """
    embeddings = calculate_embeddings(documents)
    similarities = compute_similarities(embeddings)
    plagiarism, same_theme, different = categorize_similarities(similarities)

    return plagiarism, same_theme, different
