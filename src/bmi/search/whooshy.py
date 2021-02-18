"""
 Copyright (C) 2021 Pablo Castells y Alejandro Bellogín

 Este código se ha implementado para la realización de las prácticas de
 la asignatura "Búsqueda y minería de información" de 4º del Grado en
 Ingeniería Informática, impartido en la Escuela Politécnica Superior de
 la Universidad Autónoma de Madrid. El fin del mismo, así como su uso,
 se ciñe a las actividades docentes de dicha asignatura.
"""

import whoosh
from whoosh.fields import Schema, TEXT, ID
from whoosh.formats import Format
from whoosh.qparser import QueryParser
from search import Searcher
from index import Index, Builder, TermFreq

# A schema in Whoosh is the set of possible fields in a document in
# the search space. We just define a simple 'Document' schema
Document = Schema(
        path=ID(stored=True),
        content=TEXT(vector=Format)
    )

class WhooshBuilder(Builder):
    pass
    ## TODO ##
    # Your code here #

class WhooshIndex(Index):
    def __init__(self, path):
        Index.__init__(self, index_path=path) 
    
    # Doc 
    def doc_freq(self, term):
        pass

    # All terms returns only the term info. 
    def all_terms(self):
        info = []
        for i in self.terms:
            info.append(i[0])

        return info
    
    # Concatenate the word with its frequency???
    def all_terms_with_freq(self):
        # for each : term freq
        return self.terms         

    # Frequency of a word in all documentss
    def total_freq(self, term):
        pass

    # Frequency of a single word in a document 
    def term_freq(self, term, doc_id):
        vector = index.doc_vector(doc_id)
        nTerms = vector.size()
        i = 0
        for f in vector:
            if f==term:
                i+=
         print(" Frequency of term in doc_id = " + str(doc_id) + " - " + index.doc_path(doc_id) + ": " + i)
        pass


    def doc_path(self, doc_id):
        pass

    def doc_vector(self, doc_id):
        pass

    def postings(self, word):

        return indexreader.postings().items_as()
        


class WhooshSearcher(Searcher):
    pass
    ## TODO ##
    # Your code here #
