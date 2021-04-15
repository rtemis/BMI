"""
 Copyright (C) 2021 Pablo Castells, Alejandro Bellogín y Andrés Mena

 Este código se ha implementado para la realización de las prácticas de
 la asignatura "Búsqueda y minería de información" de 4º del Grado en
 Ingeniería Informática, impartido en la Escuela Politécnica Superior de
 la Universidad Autónoma de Madrid. El fin del mismo, así como su uso,
 se ciñe a las actividades docentes de dicha asignatura.
"""

import heapq
from abc import ABC, abstractmethod


class Ratings:
    def __init__(self, file="", delim='\t'):
        """ Completar """

    def rate(self, user, item, rating):
        """ Completar """

    def rating(self, user, item):
        """ Completar """

    def random_split(self, ratio):
        """ Completar """

    """ Y completar... """


class Ranking:
    class ScoredItem:
        """
        Clase utilizada para gestionar las comparaciones que se realizan dentro del heap
        """
        def __init__(self, element):
            self.element = element

        def __lt__(self, other):
            """
            En primer lugar se compara el score. En caso de que sean iguales (mismo score),
            se compara usando el itemid (se colocará más arriba el elemento con un itemid menor).
            """
            return self.element[0] < other.element[0] if self.element[0] != other.element[0] \
                else self.element[1] > other.element[1]

        def __eq__(self, other):
            return self.element == other.element

        def __str__(self):
            return str(self.element)

        def __repr__(self):
            return self.__str__()

    def __init__(self, topn):
        self.heap = []
        self.topn = topn
        self.changed = 0

    #     self.heap = []
    #     self.topn = topn

    # def add(self, item, score):
    #     if (len(self.heap) < self.topn) or (score > self.heap[0][0]):
    #         if len(self.heap) == self.topn:
    #             heapq.heappop(self.heap)
    #         heapq.heappush(self.heap, (score, item))

    # def __iter__(self):
    #     h = self.heap.copy()
    #     ranking = []
    #     while h:
    #         ranking.append(heapq.heappop(h)[::-1])
    #     return reversed(ranking)

    def add(self, item, score):
        scored_item = self.ScoredItem((score, item))
        if len(self.heap) < self.topn:
            heapq.heappush(self.heap, scored_item)
            self.changed = 1
        elif scored_item > self.heap[0]:
            heapq.heappop(self.heap)
            heapq.heappush(self.heap, scored_item)
            self.changed = 1

    def __iter__(self):
        if self.changed:
            self.ranking = []
            h = self.heap.copy()
            while h:
                self.ranking.append(heapq.heappop(h).element[::-1])
            self.changed = 0
        return reversed(self.ranking)

    def __repr__(self):
        r = "<"
        for item, score in self:
            r = r + str(item) + ":" + str(score) + " "
        return r[0:-1] + ">"


class Recommender(ABC):
    def __init__(self, training):
        self.training = training

    def __repr__(self):
        return type(self).__name__

    @abstractmethod
    def score(self, user, item):
        """ Core scoring function of the recommendation algorithm """

    def recommend(self, topn):
        """ Completar """


class RandomRecommender(Recommender):
    def score(self, user, item):
        return random.random()


class MajorityRecommender(Recommender):
    def __init__(self, ratings, threshold=0):
        super().__init__(ratings)
        self.threshold = threshold

    def score(self, user, item):
        return sum(rating >= self.threshold for user, rating in self.training.item_users(item).items())


class UserSimilarity(ABC):
    @abstractmethod
    def sim(self, user1, user2):
        """ Computation of user-user similarity metric """


class Metric(ABC):
    def __init__(self, test, cutoff):
        self.test = test
        self.cutoff = cutoff

    def __repr__(self):
        return type(self).__name__ + ("@" + str(self.cutoff) if self.cutoff != math.inf else "")

    # Esta función se puede dejar abstracta declarándola @abstractmethod, 
    # pero también se puede meter algo de código aquí y el resto en las
    # subclases - a criterio del estudiante.
    def compute(self, recommendation):
        """ Completar """