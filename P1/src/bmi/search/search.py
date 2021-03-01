"""
 Copyright (C) 2021 Pablo Castells y Alejandro Bellogín

 Este código se ha implementado para la realización de las prácticas de
 la asignatura "Búsqueda y minería de información" de 4º del Grado en
 Ingeniería Informática, impartido en la Escuela Politécnica Superior de
 la Universidad Autónoma de Madrid. El fin del mismo, así como su uso,
 se ciñe a las actividades docentes de dicha asignatura.
"""

import math
import os
from abc import ABC, abstractmethod
from statistics import term_stats

# Calculates the tf value 
def tf(freq):
    return 1 + math.log2(freq) if freq > 0 else 0

# Calculates the idf value  
def idf(df, n):
    return math.log2((n + 1) / (df + 0.5))

# Returns the modulo for a given document
def get_mod(index, docid):
    fp = open(index.index_path + '/modulo.txt', 'r')
    details = fp.readlines()
    mod = float(details[docid].split('\t')[1])

    fp.close()
    return mod

# Creates a lookup file for the modulos of all documents
def set_mod(index):
    terms = index.all_terms()
    ndocs = index.ndocs()

    idfval = {}
    for t in terms: 
        idfval[t] = idf(index.doc_freq(t), ndocs)

    fp = open(index.index_path + '/modulo.txt', 'w')
    for doc in range (0, ndocs):
        d = math.sqrt(math.fsum([math.pow(0 if tup.info[0] not in idfval else tf(tup.info[1]) * idfval[tup.info[0]], 2) for tup in index.doc_vector(doc)]))
        fp.write(str(doc) +'\t'+ str(d) +'\n')
    fp.close()


# Parses a query returning a list of words in lower case, separated by spaces
class Parser():
    def parse(self, query):
        return query.lower().split(" ")

"""
    This is an abstract class for the search engines
"""
class Searcher(ABC):
    def __init__(self, index, parser):
        self.index = index
        self.parser = parser
    @abstractmethod
    def search(self, query, cutoff):
        """ Returns a list of documents built as a pair of path and score """


class VSMDotProductSearcher(Searcher):

    def __init__(self, engine):
        self.index = engine
        self.parser = Parser()
        # term_stats(self.index, 'dotproductSearcher.png')

    
    def search(self, query, cutoff):
        tuples = []

        query_terms = self.parser.parse(query)
        
        for doc in range(0,self.index.ndocs()):
            tfidf = 0
            for q in query_terms:
                tfidf += self.score(q, doc)       
            tuples.append([self.index.doc_path(doc), tfidf])
        tuples.sort(key=lambda tup: tup[1], reverse=True)
        return tuples[0:cutoff]
    
    # We created a score function to be able to override it when using different indices
    def score(self, term, doc):
        return tf(self.index.term_freq(term, doc)) * idf(self.index.doc_freq(term), self.index.ndocs()) 


class VSMCosineSearcher(VSMDotProductSearcher):
    def __init__(self, engine):
        self.index = engine
        self.parser = Parser()
        # Create a file to search for the modulo
        set_mod(self.index)
        # term_stats(self.index, 'vscosineSearcher.png')

    # For this score, we use the modulo document created and divide
    def score(self, term, doc):
        return ( tf(self.index.term_freq(term, doc)) * idf(self.index.doc_freq(term), self.index.ndocs()) ) / get_mod(self.index, doc)
    

