import numpy as np
import spacy

nlp = spacy.load('en_core_web_sm')


def cluster_text(text, threshold=0.3):

    def process(text):
        doc = nlp(text)
        sents = list(doc.sents)
        vecs = np.stack([sent.vector / sent.vector_norm for sent in sents])
        return sents, vecs

    def cluster(sents, vecs, threshold):
        clusters = [[0]]
        for i in range(1, len(sents)):
            if np.dot(vecs[i], vecs[i-1]) < threshold:
                clusters.append([])
            clusters[-1].append(i)
        return clusters

    def clean(text):
        # Add cleaning logic here
        return text

    sents, vecs = process(text)

    clusters = cluster(sents, vecs, threshold)

    final_texts = []
    for cluster in clusters:
        cluster_text = clean(' '.join([sents[i].text for i in cluster]))
        if 60 < len(cluster_text) < 3000:
            final_texts.append(cluster_text)

    if not final_texts:
        threshold = 0.6
        sents, vecs = process(text)
        clusters = cluster(sents, vecs, threshold)

        for cluster in clusters:
            cluster_text = clean(' '.join([sents[i].text for i in cluster]))
            if 60 < len(cluster_text) < 3000:
                final_texts.append(cluster_text)

    return final_texts
