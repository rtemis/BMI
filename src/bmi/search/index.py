"""
 Copyright (C) 2021 Pablo Castells y Alejandro Bellogín

 Este código se ha implementado para la realización de las prácticas de
 la asignatura "Búsqueda y minería de información" de 4º del Grado en
 Ingeniería Informática, impartido en la Escuela Politécnica Superior de
 la Universidad Autónoma de Madrid. El fin del mismo, así como su uso,
 se ciñe a las actividades docentes de dicha asignatura.
"""

class TermFreq():
    def __init__(self, t):
        self.info = t
    def term(self):
        return self.info[0]
    def freq(self):
        return self.info[1]


class Index:
    def __init__(self, ...):
        ## TODO ##
        # Your code here #

    def doc_freq(self, term):
        pass
        ## TODO ##
        # Your code here #
    def all_terms(self):
        pass
    
    def all_terms_with_freq(self):
        pass

    def total_freq(self, term):
        pass

    def doc_vector(self, doc_id):
        pass

    def postings(self, word):
        pass

    def TODO(self, ...):
        pass
        ## TODO ##
        # Your code here #


class Builder:
        ## TODO ##
        # Your code here #
