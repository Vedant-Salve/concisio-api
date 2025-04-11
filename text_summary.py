import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text='''Lelouch vi Britannia is an exiled Britannian prince, the son of Emperor Charles zi Britannia and his royal consort Marianne vi Britannia.
 Lelouch has a little sister, Nunnally Vi Britannia. Marianne was brutally murdered in the palace, and Nunnally, who witnessed the murder of their mother, was so traumatized that she lost her sight, and stray bullets to her lower body took away her ability to walk.
   Lelouch is furious with his father, believing he failed his mother and sister by turning a blind eye to their mother's death and failing to pursue their mother's killer.'''

def summarizer(rawdoc):
    # list of stopword
    stopwords=list(STOP_WORDS)
    # print(stopwords)

    nlp = spacy.load("en_core_web_sm")
    doc=nlp(rawdoc)
    # print(doc)

    # tokenization on text
    tokens=[token.text for token in doc]
    # print(tokens)

    # getting word and its frequency
    word_freq={}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
            else:
                word_freq[word.text]+=1

    # print(word_freq)

    # getting count of word with maximum frequency
    max_freq=max(word_freq.values())
    # print(max_freq)

    # normalizing frequencies of word by dividing every word frequency by max frequency
    for word in word_freq.keys():
        word_freq[word]=word_freq[word]/max_freq

    # print(word_freq)

    # sentence tokenization
    sent_tokens=[sent for sent in doc.sents]
    # print(sent_tokens)

    # getting sentence and summing its word frequencies from word_freq
    sent_scores={}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent]=word_freq[word.text]
                else:
                    sent_scores[sent]+=word_freq[word.text]
    # print(sent_scores)

    # how many sentence you want in your summary
    select_len=int(len(sent_tokens)*0.5)
    # print(select_len)

    # get the sentences with highest frequencies
    summary=nlargest(select_len , sent_scores , key=sent_scores.get)
    # print(summary)

    # Sort them in the original order as they appear in the text
    sorted_summary=sorted(summary,key=lambda sent: sent.start)

    # converting summary form list to text
    final_summary=[word.text for word in sorted_summary]
    summary=" ".join(final_summary)
    # print(summary)

    # print("Text: ",text)
    # print("Summary: ",summary)

    return summary,doc,len(rawdoc.split(" ")),len(summary.split(" "))