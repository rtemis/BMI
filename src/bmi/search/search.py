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

def tf(freq):
    return 1 + math.log2(freq) if freq > 0 else 0

def idf(df, n):
    return math.log2((n + 1) / (df + 0.5))

def get_mod(docid):
    fp = open(os.path.dirname() + '/index/modulo.txt', 'r')
    details = fp.readline(docid).split(' ')
    fp.close()
    return details[1]

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

        fp = open()

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
    
    def score(self, term, doc):
        return tf(self.index.term_freq(term, doc)) * idf(self.index.doc_freq(term), self.index.ndocs()) 


class VSMCosineSearcher(VSMDotProductSearcher):

    def score(self, term, doc):
        return ( tf(self.index.term_freq(term, doc)) * idf(self.index.doc_freq(term), self.index.ndocs()) )/ self.mod(doc)
