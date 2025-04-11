import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

def summarizer(rawdoc):
    stopwords = list(STOP_WORDS)
    doc = nlp(rawdoc)

    # Word frequency (excluding stopwords and punctuation)
    word_freq = {}
    for word in doc:
        word_text = word.text.lower()
        if word_text not in stopwords and word_text not in punctuation:
            word_freq[word_text] = word_freq.get(word_text, 0) + 1

    # Normalize frequencies
    max_freq = max(word_freq.values(), default=1)
    word_freq = {word: freq / max_freq for word, freq in word_freq.items()}

    # Sentence scoring
    sent_tokens = list(doc.sents)
    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text.lower() in word_freq:
                sent_scores[sent] = sent_scores.get(sent, 0) + word_freq[word.text.lower()]

    # Top n sentences
    select_len = max(1, int(len(sent_tokens) * 0.5))
    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    sorted_summary = sorted(summary, key=lambda sent: sent.start)

    final_summary = " ".join([sent.text for sent in sorted_summary])
    return final_summary, doc, len(rawdoc.split()), len(final_summary.split())
