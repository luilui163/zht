# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-06-22  16:23
# NAME:zht-zht_search_sentence.py
import os
import pickle
import re
import time
from collections import defaultdict

import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
DIR_CORPORA=r'D:\zht\database\projects\financial_paper_corpus'
DIR_PROJ= r'E:\zht_search_sentence'
P_MODEL=os.path.join(DIR_PROJ, 'model.pkl')




#TODO:make sure that there is no dupicated docoments in corpora
#TODO:handle duplicates or not？
#TODO: do not include reference in the corpora
def get_items():
    fns = os.listdir(DIR_CORPORA)
    fns = [fn for fn in fns if fn.endswith('.txt')]
    fns = [fn for fn in fns if not re.search(u'[\u4e00-\u9fff]', fn)]# do not include files with Chinese characters in file names
    fps = [os.path.join(DIR_CORPORA, fn) for fn in fns]

    items=defaultdict(list)
    paperId_mapper={}
    for iid,fp in enumerate(fps):
        sents=nltk.sent_tokenize(open(fp,encoding='utf8').read(),language='english')
        sents = [s.replace('\n', '') for s in sents]# strip '\n' in sentence
        sents = [s for s in sents if 50 <= len(s) <= 500] # delete the extremely long sentences
        for s in sents:
            items[s].append(iid) #review:duplicates
        paperId_mapper[iid]=os.path.basename(fp)
        print(iid)
    pickle.dump(items,open(os.path.join(DIR_PROJ,'items.pkl'),'wb'))
    pickle.dump(paperId_mapper,open(os.path.join(DIR_PROJ,'paperId_mapper.pkl'),'wb'))

def _valid_or_not(sent):
    '''
    determine whether the sent will be included in the corpora or not
    :param sent:
    :return:
    '''
    tokenizer=nltk.tokenize.RegexpTokenizer(r'\w+')
    tokens=tokenizer.tokenize(sent)
    for token in tokens:
        if token in stopwords.words('english'):
            tokens.remove(token)
    tokens=[t for t in tokens if len(t)>3]
    tokens=[t for t in tokens if not t.isdigit()]
    if len(tokens)>=5:# only keep tokens with more than 5 word
        return True
    else:
        return False

def filter_items():
    '''
    The raw sentences tokenized from files are messy. This function is used to
    purify the sentences to build a clean corpora
    :return:
    '''
    items=pickle.load(open(os.path.join(DIR_PROJ,'items.pkl'),'rb'))
    sents=list(items.keys())
    for i,sent in enumerate(sents):
        if not _valid_or_not(sent):
            del items[sent]
        print(i)
    pickle.dump(items,open(os.path.join(DIR_PROJ,'valid_items.pkl'),'wb'))

# get_items()
# filter_items()

def __tokenize_and_stem(sent):
    # tokens= nltk.word_tokenize(sent,language='english')
    tokenizer=nltk.tokenize.RegexpTokenizer(r'\w+')

    tokens=tokenizer.tokenize(sent)
    for token in tokens:
        if token in stopwords.words('english'):
            tokens.remove(token)

    #TODO: check the clean_tokens

    porter=nltk.PorterStemmer()
    tokens=[porter.stem(t) for t in tokens]
    # wnl=nltk.WordNetLemmatizer()
    # tokens1=[wnl.lemmatize(t) for t in tokens]
    # TODO: how to handle synonymns and antonyms
    tokens=[t for t in tokens if len(t)>=3] # filter out single number and character,'Arditti, F. D. 1971.'
    tokens=[t for t in tokens if not t.isdigit()]
    return tokens

class Result(object):
    '''
    search result
    '''
    def __init__(self,sentence,papers):
        self.sentence=sentence
        self.papers=papers

    def __repr__(self):
        result=''
        result+=self.sentence+'\n'
        for i,p in enumerate(self.papers):
            result+='\t({})--> {}\n'.format(i,p)
        return result


def build_model():
    valid_items=pickle.load(open(os.path.join(DIR_PROJ,'valid_items.pkl'),'rb'))
    indexables=[(iid,sent,paperList) for iid,(sent,paperList) in enumerate(valid_items.items())]
    tfidf_vectorizer=TfidfVectorizer(
                                     stop_words='english',
                                     min_df=1,#trick:there may be some abnormal word,use this paramter to filter out the word that only appears in one sentence
                                     # tokenizer=tokenize_and_stem, #use self defined tokenizer will be much slower
                                     # ngram_range=(1,1) # TODO: If search sentence,this parameter will be useful
                                    )
    tfidf_matrix=tfidf_vectorizer.fit_transform([m[1] for m in indexables])
    #TODO:two pattern: search vocabulary or sentence
    pickle.dump((tfidf_vectorizer,tfidf_matrix,indexables),open(P_MODEL,'wb'))

def run():
    ts=time.time()
    build_model()
    te=time.time()
    print('Indexing time is : {}'.format(te-ts))


tfidf_vectorizer,tfidf_matrix,indexables=pickle.load(open(P_MODEL,'rb'))
paperId_mapper=pickle.load(open(os.path.join(DIR_PROJ,'paperId_mapper.pkl'),'rb'))

def search(query,n=10):
    response=tfidf_vectorizer.transform([query])
    target=tfidf_matrix[:,response.nonzero()[1]].toarray()
    iids=target.sum(1).argsort()[-n:][::-1]
    items=[indexables[i] for i in iids]
    items=[(iid,sent,[paperId_mapper[paper] for paper in paperList]) for iid,sent,paperList in items]
    results=[Result(item[1],item[2]) for item in items]
    for i, r in enumerate(results):
        print('{}. {}'.format(i, str(r)))
'''
This table presents the results of univariate portfolio analyses of the relation between each of measures of market beta and future stock returns.
'''
query=r'This table presents the results of univariate portfolio analyses of the relation between each of measures of market beta and future stock returns.'

search(query,50)


#trick:why not use google search directly


