# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-06-18  19:49
# NAME:zht-Natural language processing with python.py

import nltk

nltk.data.path.append(r'D:\zht\database\nltk_data')

# nltk.download()

nltk.corpus.gutenberg.fileids()

emma=nltk.corpus.gutenberg.words('austen-emma.txt')
len(emma)

emma=nltk.Text(emma)
emma.concordance('surprize',width=200,lines=10)


from nltk.corpus import gutenberg
macbeth_sentences=gutenberg.sents('shakespeare-macbeth.txt')


from nltk.corpus import webtext
for fileid in webtext.fileids():
    print(fileid,webtext.raw(fileid)[:65],'...')

from nltk.corpus import brown
cfd=nltk.ConditionalFreqDist(
    (genre,word)
    for genre in brown.categories()
    for word in brown.words(categories=genre))
genres=['news','religion','hobbies','science_fiction','romance','humor']
modals=['can','could','may','might','must','will']
cfd.tabulate(conditions=genres,samples=modals)


from nltk.corpus import inaugural
cfd=nltk.ConditionalFreqDist(
    (target,fileid[:4])
    for fileid in inaugural.fileids()
    for w in inaugural.words(fileid)
    for target in ['america','citizen']
    if w.lower().startswith(target))
cfd.plot()


from nltk.corpus import PlaintextCorpusReader
corpus_root=r'E:\a\my_corpus'
mywordlist=PlaintextCorpusReader(corpus_root, '.*')
mywordlist.fileids()
w=mywordlist.words('text2.txt')
sents=mywordlist.sents('text1.txt')
for sent in sents[:30]:
    print(' '.join(sent))


# Generating random text with bigrams
sent=['In','the','beginning','God','created','the','heaven','and','the','earth','.']
def generate_model(cfdlist,word,num=15):
    for i in range(num):
        print(word,end=' ')
        word=cfdlist[word].max()

text=nltk.corpus.genesis.words('english-kjv.txt')
bigrams=nltk.bigrams(text)
cfd=nltk.ConditionalFreqDist(bigrams)
cfd['living']
generate_model(cfd,'living')



def unusual_words(text):
    text_vocab=set(w.lower() for w in text if w.isalpha())
    englisth_vocab=set(w.lower() for w in nltk.corpus.words.words())
    unusual=text_vocab-englisth_vocab
    return sorted(unusual)

a=unusual_words(w)


from nltk.corpus import stopwords
stopwords.words('english')


def content_fraction(text):
    stopwords=nltk.corpus.stopwords.words('english')
    content=[w for w in text if w.lower() not in stopwords]
    return len(content)/len(text)

content_fraction(nltk.corpus.reuters.words())


puzzle_letters=nltk.FreqDist('egivrvonl')
obligatory='r'
wordlist=nltk.corpus.words.words()
x=[w for w in wordlist if len(w)>=6
                        and obligatory in w
                        and nltk.FreqDist(w)<=puzzle_letters]
x


names=nltk.corpus.names
names.fileids()
male_names=names.words('male.txt')
female_names=names.words('female.txt')
x=[n for n in male_names if n in female_names]
x

cfd=nltk.ConditionalFreqDist(
    (fileid,name[-1])
    for fileid in names.fileids()
    for name in names.words(fileid))
cfd.plot()



from nltk.corpus import swadesh
swadesh.fileids()
swadesh.words('en')


from nltk.corpus import wordnet as wn
# synonym set
wn.synsets('motorcar')
wn.synset('car.n.01').lemma_names()

wn.synset('car.n.01').definition()
wn.synset('car.n.01').examples()
wn.synset('car.n.01').lemmas()
wn.lemma('car.n.01.automobile').synset()

import re
re.findall(r'^.*(ing|ly|ed|ious|ies|ive|es|s|ment)$','processing')

re.findall(r'^(.*)(ing|ly|ed|ious|ies|ive|es|s|ment)$','processing')
re.findall(r'^(.*)(ing|ly|ed|ious|ies|ive|es|s|ment)$','processes')
re.findall(r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)$','processes')
re.findall(r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)$','language')
re.findall(r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)?$','language')


def stem_old(word):
    for suffix in ['ing','ly','ed','ious','ies','ive','es','s','ment']:
        if word.endswith(suffix):
            return word[:-len(suffix)]
    return word

def stem(word):
    regexp=r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)?$'
    stm,suffix=re.findall(regexp,word)[0]
    return stm

from nltk import word_tokenize

raw = """DENNIS: Listen, strange women lying in ponds distributing swords
is no basis for a system of government.  Supreme executive power derives from
a mandate from the masses, not from some farcical aquatic ceremony."""

tokens=word_tokenize(raw)
[stem(t) for t in tokens]

