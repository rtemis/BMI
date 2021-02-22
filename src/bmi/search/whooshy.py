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
from bs4 import BeautifulSoup
from urllib.request import urlopen

# A schema in Whoosh is the set of possible fields in a document in
# the search space. We just define a simple 'Document' schema
Document = Schema(
        path=ID(stored=True),
        content=TEXT(vector=Format)
    )

class WhooshBuilder(Builder):
    def __init__(self, directory):
        self.writer = whoosh.index.create_in(directory, Document).writer()
    
    def build(self, collection):
        for doc in collection:
            self.writer.add_document(path=doc, content=BeautifulSoup(urlopen(doc).read(), "lxml").text)
        self.commit()

    def commit(self):
        self.writer.commit()

class WhooshIndex(Index):
    def __init__(self, path):
        self.reader = whoosh.index.open_dir(path).reader()

    # All terms returns only the term info. 
    def all_terms(self):
        info = []
        for i in self.reader.all_terms():
            if "\\x" not in str(i[1]):
                info.append(i[1])

        # Returning binary like in the given example
        return info
    
    # Concatenate the word with its frequency???
    def all_terms_with_freq(self):
        term_freq = []
        info = self.all_terms()

        for term in info:
            term_freq.append((term, self.reader.frequency("content", term)))
        
        return term_freq   

    # Frequency of a word in all documentss
    def total_freq(self, term):
        return self.reader.frequency("content", term)

    # Frequency of a single word in a document 
    def term_freq(self, term, doc_id): 
        vector = self.reader.vector(doc_id, "content")
        vector.skip_to(term)
        return vector.value_as("frequency")

    # Returns the total number of documents that contain "term"
    def doc_freq(self, term):
        return self.reader.doc_frequency("content", term)

    # Returns path of document given by id = doc_id
    def doc_path(self, doc_id):
        return self.reader.stored_fields(doc_id)['path']

    # Given a document returns an array of the terms associated to their frequency 
    def doc_vector(self, doc_id):
        return self.reader.vector(doc_id, "content").items_as("frequency")

    # Given a term matches every document with the frequncy of that term
    def postings(self, word):
        return self.reader.postings("content", word).items_as("frequency")
        


class WhooshSearcher(Searcher):

    def __init__(self, path):
        self.searcher = whoosh.index.open_dir(path).searcher()

