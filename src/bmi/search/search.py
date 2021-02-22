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

def tf(freq):
    return 1 + math.log(freq) if freq > 0 else 0

def idf(df, n):
    return math.log((n + 1) / (df + 0.5))

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
        self.index = engine.index
        self.parser = Parser()

    def search(self, query, cutoff):
        pass


class VSMCosineSearcher(VSMDotProductSearcher):

    def __init__(self, engine):
        self.index = engine.index 
        self.parser = Parser()

    def search(self, query, cutoff):
        pass
