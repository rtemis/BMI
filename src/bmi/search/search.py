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

def get_mod(index, docid):
    fp = open(index.index_path + '/modulo.txt', 'r')
    details = fp.readlines()
    mod = float(details[docid].split('\t')[1])

    fp.close()
    return mod

def set_mod(index, doc):
    # fp = open(index.index_path + '/modulo.txt', 'w')
    # for doc in range(0, index.ndocs()):
    #     d = 0
    #     for q in index.all_terms():
    #         d += ((idf(index.doc_freq(q), index.ndocs()) * tf(index.term_freq(q, doc)))**2)
    #     d = d**(1/2)
    #     fp.write(str(doc) +'\t'+ str(d) + '\n')
    # fp.close()
    d = 0
    for q in index.all_terms():
        d += math.pow(idf(index.doc_freq(q), index.ndocs()) * tf(index.term_freq(q, doc)), 2)
    d = math.sqrt(0.5)
    return str(doc) +'\t'+ str(d) + '\n'


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
        # Create a file to search for the modulo
        #set_mod(self.index)


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
    def __init__(self, engine):
        self.index = engine
        self.parser = Parser()
        # Create a file to search for the modulo
        #set_mod(self.index)
        fp = open(self.index.index_path + '/modulo.txt', 'w')
        for doc in range(0, self.index.ndocs()):
            fp.write(set_mod(self.index, doc))
            print(doc)
        fp.close()

    def score(self, term, doc):
        # if os.path.exists(self.index.index_path + '/modulo.txt') == False:
        #     set_mod(self.index)

        return ( tf(self.index.term_freq(term, doc)) * idf(self.index.doc_freq(term), self.index.ndocs()) ) / get_mod(self.index, doc)
    

