import heapq
import networkx
from abc import ABC, abstractmethod


class UndirectedSocialNetwork:
    def __init__(self, file, delimiter='\t', parse=0):
        self.friendshipDict = {}   #redundant but necessary structure.. if a and b are friends ->  fDict[a] = {b}    fDict[b] = {a}
        fp = open(file, "r")
        for line in fp.readlines():
            d = line.split(delimiter)
            d[1] = d[1].strip('\n')
            self.add_contact(int(d[0]), int(d[1]))
        print(self.friendshipDict)

    def users(self):
        return self.friendshipDict.keys()

    def contacts(self, user):
        return self.friendshipDict[user]

    def degree(self, user):
        return len(self.friendshipDict[user])

    def add_contact(self, u, v):
        if u not in self.friendshipDict.keys():
            self.friendshipDict[u] = []
        if v not in self.friendshipDict.keys():
            self.friendshipDict[v] = []

        self.friendshipDict[u].append(v)        
        self.friendshipDict[v].append(u)

    def connected(self, u, v):
        return (u in self.friendshipDict[v])

    def nedges(self):
        count = 0
        for u in self.friendshipDict.keys():
            for v in self.friendshipDict.keys():
                if u in self.friendshipDict[v]:
                    count += 1
        return count / 2


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

class UserClusteringCoefficient(LocalMetric):
    def __init__(self, topn):
        self.topn = topn
        self.ranking = Ranking(topn)    

    def compute(self, network, element):
        count = 0
        for u in network.contacts(element):
            for v in network.contacts(element):
                if network.connected(u,v):
                    count += 1
        count /= 2
        return count / ((len(network.contacts(element)) * (len(network.contacts(element))-1)) / 2) 
    
    def compute_all(self, network):
        for user in network.friendshipDict.keys():
            self.ranking.add(user, self.compute(network, user))
        return self.ranking.__repr__()
    

class ClusteringCoefficient(Metric):
    def compute_all(self, network):
        pass

class Embeddedness(Metric):
    def compute(self, network, element):
        u1 = element[0]
        u2 = element[1]
        neighbors = []
        for user in network.contacts(u1):
            if user in network.contacts(u2):
                neighbors.append(user)
        return len(neighbors) / (len(network.contacts(u2)) + len(network.contacts(u1)) - 2) 

class Assortativity(Metric):
    def compute(self, network):
        num1 = 0
        second_term = 0
        den1 = 0
        #TODO num1
        for user in network.users():
            second_term += (network.degree(user)) ** 2
        second_term = second_term ** 2
        for user in network.users():
            den1 += (network.degree(user)) ** 3
        den1 *= 2 * network.nedges
        return (num1 - second_term) / (den1 - second_term)


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

