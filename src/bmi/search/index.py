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


    def doc_freq(self, term):
        pass

    def all_terms(self):
        pass
    
    def all_terms_with_freq(self):
        pass

    def total_freq(self, term):
        pass

    def term_freq(self, term, doc_id):
        pass


    def doc_path(self, doc_id):
        pass

    def doc_vector(self, doc_id):
        pass

    def postings(self, word):
        pass



class Builder:

    def __init__(self, path, collection):
        pass

    def build(self, collection):
        pass

    def commit(self):
        pass


