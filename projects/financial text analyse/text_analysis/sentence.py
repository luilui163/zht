# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-06-21  14:55
# NAME:text_analysis-sentence.py

import logging
import re
import unicodedata

from search import Indexable, SearchEngine
from util import timed

logger=logging.getLogger(__name__)

class Sentence(Indexable):
    '''Class encapsulating a specific behavior of indexed sentences.'''
    def __init__(self,iid,bib,metadata):
        Indexable.__init__(self,iid,metadata)
        self.bib=bib

    def __repr__(self):
        return 'id: {}, bib: {}'.format(self.iid,self.bib)


class SentenceDataPreprocessor(object):
    '''Preprocessor for sentence entries'''
    _EXTRA_SPCE_REGEX = re.compile(r'\s+',re.IGNORECASE)
    _SPECIAL_CHAR_REGEX = re.compile(
        # detect punctuation characters
        r"(?P<p>(\.+)|(\?+)|(!+)|(:+)|(;+)|"
        # detect special characters
        r"(\(+)|(\)+)|(\}+)|(\{+)|('+)|(-+)|(\[+)|(\]+)|"
        # detect commas NOT between numbers
        r"(?<!\d)(,+)(?!=\d)|(\$+))")

    def preprocess(self,entry):
        '''Preprocess an entry to a sanitized format.

        The preprocess steps applied to the sentence entry is  the following:
          1. All non-accents are removed;
          2. Special characters are replaced by whitespaces (i.e. -, [, etc.);
          3. Punctuation marks are removed;
          4. Additional whitespaces between replaced by only the whitespaces.
        '''
        f_entry=entry.lower()
        f_entry=f_entry.replace('\t','|').strip()
        f_entry=self.strip_accents(f_entry)
        f_entry=self._SPECIAL_CHAR_REGEX.sub(' ',f_entry.decode('utf8'))
        f_entry=self._EXTRA_SPCE_REGEX.sub(' ',f_entry)
        sentence_desc=f_entry.split('|')
        return sentence_desc

    def strip_accents(self,text):
        return unicodedata.normalize('NFD',text).encode('ascii','ignore') #TODO:


class SentenceInventory(object):
    '''Class representing a inventory of sentences'''
    _SENTENCE_META_ID_INDEX=0
    _SENTENCE_META_BIB_INDEX=1
    _NO_RESULTS_MSG='Sorry, no results.'

    def __init__(self,filename):
        self.filename=filename
        self.engine=SearchEngine()

    @timed
    def load_sentences(self):
        '''Load sentences from a file name.

        This method leverages the iterable behavior of File objects that
        automatically uses buffered IO and memory management handling effctively
        large files.
        '''
        logger.info('Loading sentences from file ...')
        processor=SentenceDataPreprocessor()
        with open(self.filename,encoding='utf8') as catelog:
            for entry in catelog:
                sentence_desc=processor.preprocess(entry)
                metadata=' '.join(sentence_desc[self._SENTENCE_META_BIB_INDEX:])
                iid=sentence_desc[self._SENTENCE_META_ID_INDEX].strip()
                bib=sentence_desc[self._SENTENCE_META_BIB_INDEX].strip()
                sentence=Sentence(iid,bib,metadata)
                self.engine.add_object(sentence)
        self.engine.start()

    @timed
    def search_sentences(self,query,n_results=10):
        '''Search sentences according to provided query of terms.

        The query is executed against the indexed books, and a list of books
        compatible with the provided terms is return along with their tf-idf
        score.
        '''
        result=''
        if len(query)>0:
            result=self.engine.search(query,n_results)

        if len(result)>0:
            return '\n'.join([str(indexable) for indexable in result])
        return self._NO_RESULTS_MSG

    def sentences_count(self):
        '''Return number of sentences already in the index.'''
        return self.engine.count()