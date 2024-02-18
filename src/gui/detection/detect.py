from transformers import BertTokenizer, BertModel
import spacy
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load('en_core_web_md')

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def detect(documentos):
    def get_embedding(text):
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).detach().numpy()[0]

    def divide_in_sentences(text):
        doc = nlp(text)
        return [(sent.text.strip(), (sent[0].idx, sent[-1].idx + len(sent[-1].text))) for sent in doc.sents]

    embeddings = [[(get_embedding(sentence), pos) for sentence, pos in divide_in_sentences(doc)] for doc in documentos]

    plagiarism = []
    theme = []
    different = []

    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            for seg1, pos1 in embeddings[i]:
                for seg2, pos2 in embeddings[j]:
                    similitud = cosine_similarity([seg1], [seg2])[0][0]
                    
                    if similitud > 0.86:
                        if similitud > 0.9:
                            plagiarism.append(((i, pos1), (j, pos2), similitud))
                        else:
                            theme.append(((i, pos1), (j, pos2), similitud))
                    else:
                        different.append(((i, pos1), (j, pos2), similitud))
    return plagiarism, theme, different