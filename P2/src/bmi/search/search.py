"""
 Copyright (C) 2021 Pablo Castells y Alejandro Bellogín

 Este código se ha implementado para la realización de las prácticas de
 la asignatura "Búsqueda y minería de información" de 4º del Grado en
 Ingeniería Informática, impartido en la Escuela Politécnica Superior de
 la Universidad Autónoma de Madrid. El fin del mismo, así como su uso,
 se ciñe a las actividades docentes de dicha asignatura.
"""

import math
from abc import ABC, abstractmethod
from index import BasicParser
import heapq

def tf(freq):
    return 1 + math.log2(freq) if freq > 0 else 0

def idf(df, n):
    return math.log2((n + 1) / (df + 0.5))

class SearchRanking:
    # TODO: to be implemented as heap (exercise 1.3) #
    def __init__(self, cutoff):
        self.heap = []
        heapq.heapify(self.heap)
        self.ranking = list()
        self.cutoff = cutoff

    def push(self, docid, score):
        # Create new node
        tup = [score, docid]

        # Test to see if heapsize is greater than cutoff
        if len(self.heap) >= self.cutoff:
            # if limit reached, test score of new node
            if self.heap[0][0] > score:
                nodes = []
                nodes.append(tup)

                for x in self.heap:
                    nodes.append(heapq.heappop(self.heap))
                
                rem = tup
                for n in nodes:
                    if n[0] > rem[0]:
                        rem = n
                
                nodes.remove(rem)
                for n in nodes:
                    heapq.heappush(self.heap, n)
        else:
            heapq.heappush(self.heap, tup)
            

    def __iter__(self):
        for n in self.heap:
            self.ranking.append(heapq.heappop(self.heap))
        
        self.ranking.sort(key=lambda tup: tup[0], reverse=True)
        return self.ranking

"""
    This is an abstract class for the search engines
"""
class Searcher(ABC):
    def __init__(self, index, parser):
        self.index = index
        self.parser = parser
    @abstractmethod
    def search(self, query, cutoff) -> SearchRanking:
        """ Returns a list of documents built as a pair of path and score """


class SlowVSMSearcher(Searcher):
    def __init__(self, index, parser=BasicParser()):
        super().__init__(index, parser)

    def search(self, query, cutoff):
        qterms = self.parser.parse(query)
        ranking = SearchRanking(cutoff)
        for docid in range(self.index.ndocs()):
            score = self.score(docid, qterms)
            if score:
                ranking.push(self.index.doc_path(docid), score)
        return ranking

    def score(self, docid, qterms):
        prod = 0
        for term in qterms:
            prod += tf(self.index.term_freq(term, docid)) \
                    * idf(self.index.doc_freq(term), self.index.ndocs())
        mod = self.index.doc_module(docid)
        if mod:
            return prod / mod
        return 0

class TermBasedVSMSearcher(Searcher):
    
    def __init__(self, index, parser=BasicParser()):
        super().__init__(index, parser)

    def search(self, query, cutoff):
        qterms = self.parser.parse(query)
        ranking = SearchRanking(cutoff)
        postVals = {}
        scores = []
        
        for term in qterms:
            for doc, freq in self.index.postings(term):
                postVals[doc].append(term)

        for key, doc in postVals:
            scores.append([doc, self.score(key, doc)])
        
        scores.sort(key=lambda tup: tup[1], reverse=True)
        return scores[0:cutoff]
       

    def score(self, docid, qterms):
        prod = 0
        for term in qterms:
            prod += tf(self.index.term_freq(term, docid)) \
                    * idf(self.index.doc_freq(term), self.index.ndocs())
        mod = self.index.doc_module(docid)
        if mod:
            return prod / mod
        return 0


class DocBasedVSMSearcher(Searcher):
    # Your new code here (exercise 1.2*) #
    pass

class ProximitySearcher(Searcher):
    # Your new code here (exercise 4*) #
    pass
class PagerankDocScorer():
    def __init__(self, graphfile, r, n_iter):
        self.inConnections = {}
        self.outConnections = {}
        fp = open(graphfile, "r")
        #a->b           a is an "inconnection" of b, and b is an "outconnection" of a
        #assuming that the first one is the source and the second is the target and only two docids in each line
        for line in fp.readlines():
            var=line.split()
            self.inConnections[var[1]].append(var[0])
            self.outConnections[var[0]].append(var[1])
        fp.close()
        pages = []
        support = []
        for k in len(self.inConnections):
            pages[k]=1/len(self.inConnections)
        for n in range(n_iter):
            for k in len(self.inConnections)
        
            
        
        # Your new code here (exercise 6) #
        # Format of graphfile:
        #  node1 node2
        # TODO #
        pass
    def rank(self, cutoff):
        # TODO #
        pass
