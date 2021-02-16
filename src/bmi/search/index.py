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


class Index:
    def __init__(self):
        self.path = ""
        self.title = ""
        self.content = ""

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
    pass
        ## TODO ##
        # Your code here #
