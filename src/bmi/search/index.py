"""
 Copyright (C) 2021 Pablo Castells y Alejandro Bellogín

 Este código se ha implementado para la realización de las prácticas de
 la asignatura "Búsqueda y minería de información" de 4º del Grado en
 Ingeniería Informática, impartido en la Escuela Politécnica Superior de
 la Universidad Autónoma de Madrid. El fin del mismo, así como su uso,
 se ciñe a las actividades docentes de dicha asignatura.
 Commit test.
"""

class TermFreq():
    def __init__(self, t):
        self.info = t
    def term(self):
        return self.info[0]
    def freq(self):
        return self.info[1]

class DocVector():
    def __init__(self):
        self.vector = []
    def size(self):
        return len(self.vector) 


class Index:
    def __init__(self, index_path = "", content = ""):
        # The Index path is passed as a variable upon creation
        self.index_path = index_path
        # Content can be left blank
        self.content = content
        # Terms is a list of objects of type TermFreq
        self.terms = []

    # Returns the total number of documents that contain "term"
    def doc_freq(self, term):
        pass
    # All terms returns only the term info
    def all_terms(self):
        pass
    # Concatenate the word with its frequency
    def all_terms_with_freq(self):
        pass
    # Frequency of a word in all documents
    def total_freq(self, term):
        pass
     # Frequency of a single word in a document
    def term_freq(self, term, doc_id):
        pass

    # Returns path of document given by id = doc_id
    def doc_path(self, doc_id):
        pass
    # Given a document returns an array of the terms associated to their frequency
    def doc_vector(self, doc_id):
        pass
     # Given a term matches every document with the frequncy of that term
    def postings(self, word):
        pass



class Builder:

    def __init__(self, path, collection):
        pass

    def build(self, collection):
        pass

    def commit(self):
        pass


