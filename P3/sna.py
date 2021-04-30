import heapq
from abc import ABC, abstractmethod


class UndirectedSocialNetwork:
    def __init__(self, file, delimiter='\t', parse=0):
        self.friendshipDict = {}   #redundant but necessary structure.. if a and b are friends ->  fDict[a] = {b}    fDict[b] = {a}
        fp = open(file, "r")
        for line in fp.readlines():
                d = line.split(delimiter)
                if (d[0]) not in self.friendshipDict.keys():
                    self.friendshipDict[d[0]] = {}
                self.friendshipDict[d[0]] = d[1]
                if (d[1]) not in self.friendshipDict.keys():
                    self.friendshipDict[d[1]] = {}
                self.friendshipDict[d[1]] = d[0]
        """ Completar """

    def users(self):
        return self.friendshipDict.keys()
        """ Completar """

    def contacts(self, user):
        return self.friendshipDict[user]
        """ Completar """

    def degree(self, user):
        """ Completar """

    def add_contact(self, u, v):
        if u not in self.friendshipDict.keys():
                    self.friendshipDict[u] = {}
                self.friendshipDict[u] = v
                if v not in self.friendshipDict.keys():
                    self.friendshipDict[v] = {}
                self.friendshipDict[v] = u
        """ Completar """

    def connected(self, u, v):
        if u in self.friendshipDict[v]:
            return 1 #connected
        else:
            return 0
        """ Completar """

    def nedges(self):
        for u in self.friendshipDict.keys():
            for v in self.friendshipDict.keys():
                if u in
        """ Completar """


class Metric(ABC):
    def __repr__(self):
        return type(self).__name__

    @abstractmethod
    def compute_all(self, network):
        """" Compute metric on all users or edges of network """


class LocalMetric(Metric):
    def __init__(self, topn):
        self.topn = topn

    @abstractmethod
    def compute(self, network, element):
        """" Compute metric on one user of edge of network """


class Ranking:
    class ScoredUser:
        """
        Clase utilizada para gestionar las comparaciones que se realizan dentro del heap
        """
        def __init__(self, element):
            self.element = element

        def __lt__(self, other):
            """
            En primer lugar se compara el score. En caso de que sean iguales (mismo score),
            se compara usando el userid (se colocará más arriba el elemento con un userid menor).
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

    def add(self, user, score):
        scored_user = self.ScoredUser((score, user))
        if len(self.heap) < self.topn:
            heapq.heappush(self.heap, scored_user)
            self.changed = 1
        elif scored_user > self.heap[0]:
            heapq.heappop(self.heap)
            heapq.heappush(self.heap, scored_user)
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
        for user, score in self:
            r += str(user) + ":" + str(score) + " "
        return r[0:-1] + ">"

