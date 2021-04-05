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
            for doc in self.index.postings(term):
                # Calculate the partial score for that term
                if doc[0] not in postVals:
                    postVals[doc[0]] = 0  #append score here. Postvals could be a dict. of docids and score.  Then we should just push this dict. in SearchRank
                
                postVals[doc[0]] += self.score(doc[0], term)

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
            mod = self.index.doc_module(key)
            ranking.push(key, postVals[key]/mod)

        # Return the new list
        return ranking.score(self.index)
       

    def score(self, docid, term):
        return tf(self.index.term_freq(term, docid)) \
                    * idf(self.index.doc_freq(term), self.index.ndocs())


class DocBasedVSMSearcher(Searcher):
    def __init__(self, index, parser=BasicParser()):
        super().__init__(index, parser)
        self.postingsHeap = []
        heapq.heapify(self.postingsHeap)
        
    # Your new code here (exercise 1.2*) #
    def search(self, query, cutoff):
        qterms = self.parser.parse(query)
        ranking = SearchRanking(cutoff)
        k = 0
        y = 0
        temp = 0
        score = {}
        allPostings = []
        support_allPostings = []
        # Leah testings
#        scores = {}

#        for term in qterms:
 #           for post in self.index.postings(term):
  #              if post[0] in scores:

        for i, term in enumerate(qterms):
            for post in self.index.postings(term):
                allPostings.append([post[0], post[1], i])  #[0] is the docid, [1] is the freq, and k is just the indices of the query term
            k += 1
            
        allPostings.sort(key=lambda tup: tup[0], reverse=False) #order the array of all the postings from the smallest to the biggest docid
        #inizialize the postings' heap
        
        support_allPostings = allPostings

        for j in range(len(qterms)):    
            for tup in support_allPostings:
                if j == tup[2]:
                    heapq.heappush(self.postingsHeap, tup) #push the tuple in the tree
                    allPostings.remove(tup)
                    break
        
        fOutTup = heapq.heappop(self.postingsHeap)
        temp = fOutTup[1]
        
        for inTup in support_allPostings:
            if fOutTup[2] == inTup[2]:
                heapq.heappush(self.postingsHeap, inTup)
                allPostings.remove(inTup)
                break

        while(y < k):
            print (y,k)
            if len(self.postingsHeap) == 0:
                break
            sOutTup = heapq.heappop(self.postingsHeap)
            print(fOutTup, sOutTup)
            
            if sOutTup[0] == fOutTup[0]:
                temp += sOutTup[1]
            else:
                score[fOutTup[0]] = temp / self.index.doc_module(fOutTup[0])
                temp = sOutTup[1]
            
            if len(support_allPostings) != 0:
                for inTup in support_allPostings:
                    if sOutTup[2] == inTup[2]:  #push a posting for the same term
                        heapq.heappush(self.postingsHeap, inTup)
                        allPostings.remove(inTup)
                        break
            else:  #postings list is empty and the tree has exactly len(query) nodes. I just have to count these iterations and finish
                y += 1
            fOutTup = sOutTup

        for key in score:
            ranking.push(key, score[key])
        
        return ranking.score(self.index) #return a searchRanking also here.
    

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
        # Begin iterations
        for n in range(n_iter):
            for k in keys:
                self.p_p[k] = (1-r) / N 
            for i in self.outConnections:
                for j in self.outConnections[i]:
                    self.p_p[j] += (r * self.p[i] / len(self.outConnections[i])) + (r * self.p[i] * len(sinks) / N)
            for k in keys:
                self.p[k] = self.p_p[k]           
           
 

    def rank(self, cutoff):
        scores = []
        for k in self.p:
            scores.append([self.p[k], k])
        scores.sort(key=lambda tup: tup[0], reverse=True)
        return scores[:cutoff]
