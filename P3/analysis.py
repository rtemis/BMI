
from abc import ABC, abstractmethod


def main():
    friendshipDict = {}   #redundant but necessary structure.. if a and b are friends ->  fDict[a] = {b}    fDict[b] = {a}
    fp = open("graph/small1.csv", "r")
    print(fp)
    for line in fp.readlines():
        d = line.split()
        d[1] = d[1].strip('\n')
        if d[0] not in friendshipDict.keys():
            friendshipDict[d[0]] = []
        if v not in friendshipDict.keys():
            friendshipDict[d[1]] = []

        friendshipDict[d[0]].append(d[1])        
        friendshipDict[d[1]].append(d[0])
    print(friendshipDict)