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


porter=nltk.PorterStemmer()
lancester=nltk.LancasterStemmer()
p=[porter.stem(t) for t in tokens]
l=[lancester.stem(t) for t in tokens]
p
l


class IndexedText(object):
    def __init__(self,stemmer,text):
        self._text=text
        self._stemmer=stemmer
        self._index=nltk.Index((self._stem(word),i)
                               for (i,word) in enumerate(text))

    def concordance(self,word,width=40):
        key=self._stem(word)
        wc=int(width/4)
        for i in self._index[key]:
            lcontext=' '.join(self._text[i-wc:i])
            rcontext=' '.join(self._text[i:i+wc])
            ldisplay='{:>{width}}'.format(lcontext[-width:],width=width)
            rdisplay='{:{width}}'.format(rcontext[:width],width=width)
            print(ldisplay,rdisplay)

    def _stem(self,word):
        return self._stemmer.stem(word).lower()

porter=nltk.PorterStemmer()
grail=nltk.corpus.webtext.words('grail.txt')
text=IndexedText(porter,grail)
text.concordance('lie')


'''
The wordnet lemmatizer only removes affixes if the resulting word is in its 
dictionary. This additional checking process makes the lemmatizer slower than 
the above stemmers. Notice that it doesn't handle "lying", but it converts 
"women" to "woman".
'''

wnl=nltk.WordNetLemmatizer()
l=[wnl.lemmatize(t) for t in tokens]
l



raw = """'When I'M a Duchess,' she said to herself, (not in a very hopeful tone
though), 'I won't have any pepper in my kitchen AT ALL. Soup does very
well without--Maybe it's always pepper that makes people hot-tempered,'..."""

re.split(r' ',raw)
re.split(r'[ \t\n]+',raw)
re.split(r'\s+',raw)
re.split(r'\W+',raw)
re.findall(r'\w+|\S\w*',raw)
print(re.findall(r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*", raw))

text = 'That U.S.A. poster-print costs $12.40...'
pattern = r'''(?x)    # set flag to allow verbose regexps
    ([A-Z]\.)+        # abbreviations, e.g. U.S.A.
  | \w+(-\w+)*        # words with optional internal hyphens
  | \$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
  | \.\.\.            # ellipsis
  | [][.,;"'?():-_`]  # these are separate tokens; includes ], [
'''
nltk.regexp_tokenize(text, pattern)


import pprint
text=nltk.corpus.gutenberg.raw('chesterton-thursday.txt')
sents=nltk.sent_tokenize(text)
pprint.pprint(sents[79:89])



def segment(text, segs):
    words = []
    last = 0
    for i in range(len(segs)):
        if segs[i] == '1':
            words.append(text[last:i+1])
            last = i+1
    words.append(text[last:])
    return words


def evaluate(text, segs):
    words = segment(text, segs)
    text_size = len(words)
    lexicon_size = sum(len(word) + 1 for word in set(words))
    return text_size + lexicon_size


from random import randint

def flip(segs, pos):
    return segs[:pos] + str(1-int(segs[pos])) + segs[pos+1:]

def flip_n(segs, n):
    for i in range(n):
        segs = flip(segs, randint(0, len(segs)-1))
    return segs

def anneal(text, segs, iterations, cooling_rate):
    temperature = float(len(segs))
    while temperature > 0.5:
        best_segs, best = segs, evaluate(text, segs)
        for i in range(iterations):
            guess = flip_n(segs, round(temperature))
            score = evaluate(text, guess)
            if score < best:
                best, best_segs = score, guess
        score, segs = best, best_segs
        temperature = temperature / cooling_rate
        print(evaluate(text, segs), segment(text, segs))
    print()
    return segs
text = "doyouseethekittyseethedoggydoyoulikethekittylikethedoggy"
seg1 = "0000000000000001000000000010000000000000000100000000000"
anneal(text, seg1, 5000, 1.2)




def tabulate(cfdist, words, categories):
    print('{:16}'.format('Category'), end=' ')                    # column headings
    for word in words:
        print('{:>6}'.format(word), end=' ')
    print()
    for category in categories:
        print('{:16}'.format(category), end=' ')                  # row heading
        for word in words:                                        # for each word
            print('{:6}'.format(cfdist[category][word]), end=' ') # print table cell
        print()                                                   # end the row

from nltk.corpus import brown
cfd=nltk.ConditionalFreqDist(
    (genre,word)
    for genre in brown.categories()
    for word in brown.words(categories=genre))

genres=['news','religion','hobbies','science_fiction','romance','humor']
modals=['can','could','may','might','must','will']
tabulate(cfd,modals,genres)


def gender_features(word):
    return {'last_letter':word[-1]}

from nltk.corpus import names
labeled_names=([(name,'male') for name in names.words('male.txt')])+\
              [(name,'female') for name in names.words('female.txt')]

import random
random.shuffle(labeled_names)

featuresets=[(gender_features(n),gender) for (n,gender) in labeled_names]
train_set,test_set=featuresets[500:],featuresets[:500]
classifier=nltk.NaiveBayesClassifier.train(train_set)
classifier.classify(gender_features('Neo'))
classifier.classify(gender_features('Trinity'))
print(nltk.classify.accuracy(classifier,test_set))
classifier.show_most_informative_features(5)


from nltk.corpus import movie_reviews
documents=[(list(movie_reviews.words(fileid)),category)
           for category in movie_reviews.categories()
           for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)

all_words=nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features=list(all_words)[:2000]

def document_features(document):
    document_words=set(document)
    features={}
    for word in word_features:
        features['contains({})'.format(word)]=(word in document_words)
    return features

print(document_features(movie_reviews.words('pos/cv957_8737.txt')))

featuresets=[(document_features(d),c) for (d,c) in documents]
train_set,test_set=featuresets[100:],featuresets[:100]
classifier=nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier,test_set))

classifier.show_most_informative_features(5)


tagged_sents=brown.tagged_sents(categories='news')


sents=nltk.corpus.treebank_raw.sents()
tokens=[]
boundaries=set()
offset=0
for sent in sents:
    tokens.extend(sent)
    offset+=len(sent)
    boundaries.add(offset-1)

def punct_features(tokens,i):
    return {'next-word-capitalized':tokens[i+1][0].isupper(),
            'pre-word':tokens[i-1].lower(),
            'punct':tokens[i],
            'prev-word-is-one-char':len(tokens[i-1])==1}

featuresets=[(punct_features(tokens,i),(i in boundaries))
             for i in range(1,len(tokens)-1)
             if tokens[i] in '.?!']

size=int(len(featuresets)*0.1)
train_set,test_set=featuresets[size:],featuresets[:size]
classifier=nltk.NaiveBayesClassifier.train(train_set)
nltk.classify.accuracy(classifier,test_set)

def setment_sentences(words):
    start=0
    sents=[]
    for i,word in enumerate(words):
        if word in '.?!' and classifier.classify(punct_features(words,i))==True:
            sents.append(words[start:i+1])
            start=i+1
    if start<len(words):
        sents.append(words[start:])
    return sents
