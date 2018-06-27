# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-06-19  16:31
# NAME:zht-find_n_closest_sentences.py
import time

import os
import nltk
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import ward,dendrogram
import matplotlib.pyplot as plt
import numpy as np


def tokenize_and_stem(sent):
    stemmer = nltk.stem.snowball.SnowballStemmer('english')
    tokens=[word for word in nltk.word_tokenize(sent)]
    filtered_tokens=[]
    # filter out any tokens not containing letters( e.g., numberic tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]',token):
            filtered_tokens.append(token)
    stems=[stemmer.stem(t) for t in filtered_tokens]
    return stems

def tokenize_only(sent):
    tokens = [word for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters( e.g., numberic tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


def get_dist(sents):
    totalvocab_stemmed=[]
    totalvocab_tokenized=[]
    for i in sents:
        words_stemmed=tokenize_and_stem(i)
        totalvocab_stemmed.extend(words_stemmed)

        words_tokenized=tokenize_only(i)
        totalvocab_tokenized.extend(words_tokenized)

    # vocab_frame = pd.DataFrame({'words': totalvocab_tokenized},
    #                            index=totalvocab_stemmed)

    tfidf_vectorizer=TfidfVectorizer(
                                     stop_words='english',
                                     use_idf=True,
                                     tokenizer=tokenize_and_stem,
                                     ngram_range=(1,3))
    tfidf_matrix=tfidf_vectorizer.fit_transform(sents)
    # terms=tfidf_vectorizer.get_feature_names()
    dist=1-cosine_similarity(tfidf_matrix)
    return dist

def hierarchy_cluster(sents):
    dist=get_dist(sents)
    linkage_matrix=ward(dist)
    fig,ax=plt.subplots(figsize=(15,20))
    ax=dendrogram(linkage_matrix,
                  orientation='right',
                  # truncate_mode='lastp', #show only the last p merged clusters
                  # p=12, # show only the last p merged clusters
                  # show_leaf_counts=True, # otherwise numbers in brakets are counts
                  # show_contracted=True, # to get a distribution impression in truncated branches
                  )

    plt.tick_params(axis='x',
                    which='both',
                    bottom='off',
                    top='off',
                    labelbottom='off',
                    )
    plt.tight_layout()
    plt.savefig(r'e:\a\sentence_cluster.png',dpi=200)

def get_closest_n_sentences(sent,sents,n=5):
    dist=get_dist(sents)
    ind=sents.index(sent)
    d = dist[ind, :]
    indices = np.argsort(d)[:n]
    return [sents[i] for i in indices]

def get_sents():
    directory=r'D:\zht\database\projects\financial_paper_corpus'
    fns=os.listdir(directory)[:50]#TODO:
    fns=[fn for fn in fns if fn.endswith('.txt')]
    txts=[open(os.path.join(directory,fn),encoding='utf8').read() for fn in fns]
    text=''.join(txts)
    text=text.replace('\r\n','').replace('\r','').replace('\n','')
    sents=nltk.sent_tokenize(text)
    sents=sorted(list(set(sents)),key=len)
    return sents

if __name__ == '__main__':
    sents=get_sents()
    sents=[s for s in sents if len(s)>20]
    # test_sents=[s for s in sents if 300>len(s)>150]

    with open(r'e:\a\result1.txt', 'w', encoding='utf8') as f:
        for i in range(0,len(sents),int(len(sents)/10)):
            t = time.time()
            result = get_closest_n_sentences(sents[i], sents)
            f.write('='*20+sents[i]+'\n')
            f.write('\n'.join(result))
            f.write('\n\n')
            print(i,time.time() - t)

#TODO: only comapre the target sentence with the corpus

