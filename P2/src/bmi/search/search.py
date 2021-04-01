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
import itertools 

def tf(freq):
    return 1 + math.log2(freq) if freq > 0 else 0

def idf(df, n):
    return math.log2((n + 1) / (df + 0.5))

class SearchRanking:
    # TODO: to be implemented as heap (exercise 1.3) #
    def __init__(self, cutoff):
        self.heap = []
        heapq.heapify(self.heap)
        self.ranking = []
        self.cutoff = cutoff

    def push(self, docid, score):
        # Create new node
        tup = [score, docid]

        # Test to see if heapsize is greater than cutoff
        if len(self.heap) > self.cutoff:
            # if limit reached, test score of new node
            if self.heap[0][0] > score:
                nodes = []
                nodes.append(tup)

                while self.heap != []:
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
        min_l = min(len(self.ranking), self.cutoff)
        ## sort ranking
        self.ranking.sort(key=lambda tup: tup[1], reverse=True)
        return iter(self.ranking[0:min_l])

    def score(self, index):
        while self.heap != []:
            self.ranking.append(heapq.heappop(self.heap))
        
        # Inverse sort by score
        self.ranking.sort(key=lambda tup: tup[0], reverse=True)
        retList = []
        for s in self.ranking:
            retList.append([index.doc_path(s[1]), s[0]])

        return retList

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
        # Parse query
        qterms = self.parser.parse(query)
        # Create ranking tool
        ranking = SearchRanking(cutoff)
        # For all docs, calculate score
        for docid in range(self.index.ndocs()):
            score = self.score(docid, qterms)
            if score != 0:
                ranking.push(docid, score)

        # Return the new list
        return ranking.score(self.index)

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
        # Parse terms of query
        qterms = self.parser.parse(query)
        # Create ranking tool (heap size of cutoff)
        ranking = SearchRanking(cutoff)
        # Create dictionary to store rankings
        postVals = {}
        
        # For each term in the query 
        for term in qterms:
            # For each doc in the postings list for that term
            for doc, freq in self.index.postings(term):
                # Calculate the partial score for that term
                if doc in postVals:
                    postVals[doc] += self.score(doc, term)  #append score here. Postvals could be a dict. of docids and score.  Then we should just push this dict. in SearchRank
                else:
                    postVals[doc] = self.score(doc, term)

        # ------------------------------ #
        #for term in qterms:
            # For each doc in the postings list for that term
        #    for doc in self.index.postings(term):
        #        if doc not in postVals:
        #            postVals[doc] = 0  
        #        postVals[doc] += self.score(doc, term)
        # ------------------------------- #  

        # Rank each of the scores obtained in the loop
        for key in postVals:
            # Heap automatically adjusts to the size of the cutoff list
            ranking.push(key, postVals[key])

        # Return the new list
        return ranking.score(self.index)
       

    def score(self, docid, term):
        return tf(self.index.term_freq(term, docid)) \
                    * idf(self.index.doc_freq(term), self.index.ndocs())


class DocBasedVSMSearcher(Searcher):
    def __init__(self, index, parser=BasicParser()):
        super().__init__(index, parser)
    
    # Your new code here (exercise 1.2*) #
    def search(self, query, cutoff):
        qterms = self.parser.parse(query)
        ranking = SearchRanking(cutoff)
        
        for term in qterms:
            for doc, freq in self.index.postings(term):
                ranking.push(doc, )

        scores = ranking.score()

        return scores #return a searchRanking also here.
    

class ProximitySearcher(Searcher):
    # Your new code here (exercise 4*) #
    pass
class PagerankDocScorer():

    def __init__(self, graphfile, r, n_iter):
        # Set up connection lists
        self.inConnections = {}
        self.outConnections = {}

        # a->b           a is an "inconnection" of b, and b is an "outconnection" of a
        # assuming that the first one is the source and the second is the target and only two docids in each line
 
        fp = open(graphfile, "r")

        for line in fp.readlines():
            var = line.split()
            
            # Test to see if connection variable exists 
            if var[1] not in self.inConnections: 
                self.inConnections[var[1]] = []

            if var[0] not in self.outConnections: 
                self.outConnections[var[0]] = []

            # Append to list of connections 
            self.inConnections[var[1]].append(var[0])
            self.outConnections[var[0]].append(var[1])

        fp.close()

        #keys = list(lambda x, y: x.union(y.keys()), [self.inConnections, self.outConnections], set())
        keys = self.inConnections.keys() | self.outConnections.keys()
        # List of P
        self.p = {}
        # List of P'
        self.p_p = {}
        
        N = len(keys)
        
        # Initialize all values of P
        for k in keys:
            self.p[k] = 1/N
        #print(self.outConnections)
        sinks = self.inConnections.keys() - self.outConnections.keys()
        print(sinks)
        print(len(sinks))
        # Begin iterations
        for n in range(n_iter):
            for k in keys:
                self.p_p[k] = r/N 
            for i in self.outConnections:
                for j in self.outConnections[i]:
                    self.p_p[j] += ((1-r) * self.p[i] / len(self.outConnections[i])) + ((1-r) * self.p[i] * len(sinks) / N)
            for k in keys:
                self.p[k] = self.p_p[k]    
        x=0
        for k in keys:
            x += self.p[k]
        print("Sum of all the rankings is", x , "(should be 1)")        
           
 

    def rank(self, cutoff):
        scores = []
        for k in self.p:
            scores.append([self.p[k], k])
        scores.sort(key=lambda tup: tup[0], reverse=True)
        return scores[:cutoff]
