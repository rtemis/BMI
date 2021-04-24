"""
 Copyright (C) 2021 Pablo Castells, Alejandro Bellogín y Andrés Mena

 Este código se ha implementado para la realización de las prácticas de
 la asignatura "Búsqueda y minería de información" de 4º del Grado en
 Ingeniería Informática, impartido en la Escuela Politécnica Superior de
 la Universidad Autónoma de Madrid. El fin del mismo, así como su uso,
 se ciñe a las actividades docentes de dicha asignatura.
"""

import heapq
import random
import math 
from abc import ABC, abstractmethod



class Ratings:
    def __init__(self, file="", delim='\t'):
        self.userDict = {}
        self.itemDict = {}

        with open(file, 'r') as fp:
            for line in fp.readlines():
                d = line.split(delim)
                if int(d[0]) not in self.userDict.keys():
                    self.userDict[int(d[0])] = {}
                self.userDict[int(d[0])][int(d[1])] = float(d[2])
                if int(d[1]) not in self.itemDict.keys():
                    self.itemDict[int(d[1])] = {}
                self.itemDict[int(d[1])][int(d[0])] = float(d[2])


    def rate(self, user, item, rating):
        if user not in self.userDict.keys():
            self.userDict[user] = {}
        self.userDict[user][item] = rating

    def rating(self, user, item):
        if item in self.userDict[user].keys():
            return self.userDict[user][item]
        return 0

    def random_split(self, ratio):
        all_records = []

        for user in self.userDict.keys():
            for item in self.userDict[user].keys():
                all_records.append([user, item, self.userDict[user][item]])

        split = int(ratio*len(all_records))

        random.shuffle(all_records)

        return all_records[:split], all_records[split:]

    def nratings(self):
        ratings = 0
        for user in self.userDict.keys():
            ratings += len(self.userDict[user].keys())

        return ratings

    def users(self):
        return self.userDict.keys()

    def items(self):
        return self.itemDict.keys()

    def user_items(self, user):
        return self.userDict[user]
    
    def item_users(self, item):
        return self.itemDict[item]


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
        self.ranking = []
        if self.changed:
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
    

class AverageRecommender(Recommender):
    def __init__(self, ratings, min):
        super().__init__(ratings)
        self.min = min
    
    def recommend(self,topn):
        ratingsDict = {}
        userRatings = {}
        for i in self.training.itemDict.keys():
            avg = 0
            for u in self.training.itemDict[i]:
                avg += self.score(u, i)
            
            if len(self.training.itemDict[i]) >= self.min: 
                ratingsDict[i] = avg/len(self.training.itemDict[i]) 
        for user in self.training.userDict.keys():
            ranking = Ranking(topn)
            for item in ratingsDict.keys():
                if item not in self.training.userDict[user].keys():
                    ranking.add(item, ratingsDict[item])
            userRatings[user] = ranking.__repr__()
        return userRatings

    def score(self, user, item):
        return self.training.itemDict[item][user]
        #return sum((rating for rating in self.training.itemDict[item][user]) / len(self.training.itemDict[item].keys()))
    

class RandomRecommender(Recommender):
    def score(self, user, item):
        return random.random()
    def recommend(self,topn):
        userRatings = {}
        for user in self.training.userDict.keys():
            ranking = Ranking(topn)
            for item in self.training.itemDict.keys():
                if item not in self.training.userDict[user].keys():
                    ranking.add(item, self.score(user,item))
            userRatings[user] = ranking.__repr__()
        return userRatings


class MajorityRecommender(Recommender):
    def __init__(self, ratings, threshold=0):
        super().__init__(ratings)
        self.threshold = threshold

    def score(self, user, item):
        return sum(rating >= self.threshold for user, rating in self.training.item_users(item).items())
    
    def recommend(self,topn):
        userRatings = {}
        for user in self.training.userDict.keys():
            ranking = Ranking(topn)
            for item in self.training.itemDict.keys():
                if item not in self.training.userDict[user].keys():
                    ranking.add(item, self.score(user,item))
            userRatings[user] = ranking.__repr__()
        return userRatings

class UserKNNRecommender(Recommender):
    def __init__(self, ratings, sim, k):
        super().__init__(ratings)
        self.sim = sim
        self.k = k
    def score(self, user, item):
        similarities = []
        for user2 in self.training.itemDict[item].keys():
            similarities.append([self.sim.sim(user,user2),user2])
        similarities.sort(key=lambda tup: tup[0], reverse=True)
        #TODO for the first example is ok, but how we're handling the first top k element?   #for tup in similarities[:k]:   
        return sum(simv * self.training.itemDict[item][v] for simv, v in similarities) 
    
    def recommend(self,topn):
        userRatings = {}
        for user in self.training.userDict.keys():
            ranking = Ranking(topn)
            for item in self.training.itemDict.keys():
                if item not in self.training.userDict[user].keys():
                    ranking.add(item, self.score(user,item))
            userRatings[user] = ranking.__repr__()
        return userRatings

class NormUserKNNRecommender(Recommender):   #working with wrong output, the sum of the similarities it's <1 and all the NORMrecommendations are higher than the NOT-NORMrecommendations( they shoud be all lower).
    def __init__(self, ratings, sim, k, min):
        super().__init__(ratings)
        self.sim = sim
        self.k = k
        self.min = min
    def score(self, user, item):
        x=0
        similarities = []
        for user2 in self.training.itemDict[item].keys():
            if len(self.training.userDict[user2].keys()) >= self.k:
                similarities.append([self.sim.sim(user,user2),user2])
                #print('similarity between user',user,'and user',user2, 'is',self.sim.sim(user,user2) )   debugging, please leave it here unless you don't fix it
                x += self.sim.sim(user,user2)  #sum of all the similarities(referring to only one item)
            else:
                similarities.append([0,user2])
        #print('244',user, x)   debugging, please leave it here unless you don't fix it
        similarities.sort(key=lambda tup: tup[0], reverse=True)
        
        #for simv, v in similarities:
            #print('248',simv,self.training.itemDict[item][v],v,item)  debugging, please leave it here unless you don't fix it
        if x == 0:
            return (sum(simv * self.training.itemDict[item][v] for simv, v in similarities))  
        return (sum(simv * self.training.itemDict[item][v] for simv, v in similarities)) / x  #normalizing for that sum, if I sum all the "simv" parameters it's the same result
    
    def recommend(self,topn):
        userRatings = {}
        for user in self.training.userDict.keys():
            ranking = Ranking(topn)
            for item in self.training.itemDict.keys():
                if item not in self.training.userDict[user].keys():
                    ranking.add(item, self.score(user,item))
            userRatings[user] = ranking.__repr__()
        return userRatings

# class ItemNNRecommender(Recommender):
#     def __init__(self, ratings, sim, k):
#         super().__init__(ratings)
#         self.sim = sim
#         self.k = k
#     def score(self, user, item):
#         similarities = []
#         for user2 in self.training.itemDict[item].keys():
#             similarities.append([self.sim.sim(user,user2),user2])
#         similarities.sort(key=lambda tup: tup[0], reverse=True)
#         #TODO for the first example is ok, but how we're handling the first top k element?   #for tup in similarities[:k]:   
#         return sum(simv * self.training.itemDict[item][v] for simv, v in similarities) 
    
#     def recommend(self,topn):
#         itemRatings = {}
#         for item in self.training.itemDict.keys():
#             ranking = Ranking(topn)
#             for user in self.training.userDict.keys():
#                 if user not in self.training.itemDict[item].keys():
#                     ranking.add(user, self.score(user,item))
#             itemRatings[item] = ranking.__repr__()
#         return itemRatings


class ItemSimilarity(ABC):
    def __init__(self, training):
        self.training = training
    @abstractmethod
    def itemSim(self, item1, item2):
        """ Computation of item-item similarity metric """

class CosineItemSimilarity(ItemSimilarity):
    def itemSim(self, item1, item2):
        num = 0
        x = 0
        den = 0
        den1 = 0
        den2 = 0
        users = []
        for user in self.training.itemDict[item1].keys():
            if user in self.training.itemDict[item2].keys():
                users.append(user)
        for user in users:
            num += self.training.itemDict[item1][user] * self.training.itemDict[item2][user]
        for user in self.training.itemDict[item1].keys():
            x = (self.training.itemDict[item1][user]) * (self.training.itemDict[item1][user])
            den1 += x
        for user in self.training.itemDict[item2].keys():
            x = (self.training.itemDict[item2][user]) * (self.training.itemDict[item2][user])
            den2 += x
        if den1 == 0 or den2 == 0:
            return 0
        return num / (float(den) ** 0.5)

class UserSimilarity(ABC):
    def __init__(self, training):
        self.training = training
    @abstractmethod
    def sim(self, user1, user2):
        """ Computation of user-user similarity metric """    

class CosineUserSimilarity(UserSimilarity):
    def sim(self, user1, user2):
        num = 0
        x = 0
        den = 0
        den1 = 0
        den2 = 0
        items = []
        for item in self.training.userDict[user1].keys():
            if item in self.training.userDict[user2].keys():
                items.append(item)
        for item in items:
            num += self.training.userDict[user1][item] * self.training.userDict[user2][item]
        for item in self.training.userDict[user1].keys():
            x = (self.training.userDict[user1][item]) * (self.training.userDict[user1][item]) #** 2
            den1 += x
        for item in self.training.userDict[user2].keys():
            x = (self.training.userDict[user2][item]) * (self.training.userDict[user2][item]) #** 2
            den2 += x
        den = den1 * den2
        if den1 == 0 or den2 == 0:
            return 0
        return num / (float(den) ** 0.5)
    

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