#!/usr/bin/env python3

import random
import time
import sys
import math
import copy

class Ant:
    def __init__(self, graph, size):
        self.n = size
        self.graph = graph
        self.tour = [ None ] * size
        self.visited = [ False ] * size

    def visitTown(self, currentIndex, town):
        self.tour[ currentIndex + 1 ] = town
        self.visited[ town ] = True

    def isVisited(self, i):
        return self.visited[i]

    def tourLength(self):
        length = self.graph[ self.tour[self.n - 1]][ self.tour[0] ]
        for i in range(self.n - 1):
            length += self.graph[ self.tour[i] ][ self.tour[i + 1] ]
        return length

    def clear(self):
        for i in range(self.n):
            self.visited[i] = False

class AntTsp:

    def __init__(self):
        self.c = 1.0
        self.alpha = 1
        self.beta = 5
        self.evaporation = 0.5
        self.Q = 500
        self.numAntsFactor = 0.8
        self.pr = 0.01

        self.maxIterations = 2000

        self.n = 0
        self.m = 0
        self.graph = []
        self.ants = []

        self.currentIndex = 0

        self.bestTour = None
        self.bestTourLength = 0

    def readData(self, filename):
        inputFile = open(filename, 'r')
        for line in inputFile:
            tmp = list(map(int, line.split(",")))
            self.graph.append(tmp)
        inputFile.close()

        self.n = len(self.graph)
        self.m = int(self.n * self.numAntsFactor)

        self.trails = [ [0] * self.n ] * self.n
        self.probs = [0] * self.n
        for i in range(self.m):
            self.ants.append( Ant(self.graph, self.n))

    def probToAnt(self, ant):
        i = ant.tour[self.currentIndex]
        demon = 0.0

        for l in range(self.n):
            if ant.isVisited(l) == False:
                demon += math.pow(self.trails[i][l], self.alpha) * math.pow(1.0 / self.graph[i][l], self.beta)

        for j in range(self.n):
            if ant.isVisited(j):
                self.probs[j] = 0.0
            else:
                numerator = math.pow(self.trails[i][j], self.alpha) * math.pow(1.0 / self.graph[i][j], self.beta)
                self.probs[j] = numerator / demon

    def selectNextTown(self, ant):
        if random.random() < self.pr:
            t = random.randint(0, self.n - 1 - self.currentIndex)
            j = -1
            for i in range(self.n):
                if ant.isVisited(i) == False:
                    j += 1
                if j == t:
                    return i

        self.probToAnt(ant)
        r = random.random()
        tot = 0.0
        for i in range(self.n):
            tot += self.probs[i]
            if tot >= r:
                return i
        raise ValueError('Not supposed to get here.')

    def updateTrail(self):
        for i in range(self.n):
            for j in range(self.n):
                self.trails[i][j] *= self.evaporation

        for ant in self.ants:
            contribution = self.Q / ant.tourLength()
            for i in range(self.n - 1):
                self.trails[ ant.tour[i] ][ ant.tour[i + 1] ] += contribution
            self.trails[ ant.tour[n - 1] ][ant.tour[0]] += contribution

    def moveAnts(self):
        print("total:", self.n - 1)
        while (self.currentIndex < self.n - 1):
            print("currentIndex:", self.currentIndex)
            for ant in self.ants:
                ant.visitTown(self.currentIndex, self.selectNextTown(ant))
            self.currentIndex += 1

    def setupAnts(self):
        self.currentIndex = -1
        for i in range(self.m):
            self.ants[i].clear()
            self.ants[i].visitTown(self.currentIndex, random.randint(0, self.n - 1))
        self.currentIndex += 1

    def updateBest(self):
        if self.bestTour == None:
            self.bestTour = self.ants[0].tour
            self.bestTourLength = self.ants[0].tourLength()

        for ant in self.ants:
            tmpLen = ant.tourLength
            if tmpLen < self.bestTourLength:
                self.bestTourLength = tmpLen
                self.bestTour = copy.deepcopy(ant.tour)

    def solve(self):
        for i in range(self.n):
            for j in range(self.n):
                self.trails[i][j] = self.c

        iteration = 0
        while iteration < self.maxIterations:
            print("Iteration:", iteration)
            self.setupAnts()
            print("en setup")
            self.moveAnts()
            print("end move")
            self.updateTrails()
            print("end update trails")
            self.updateBest()
            print("end update best")
            iteration += 1

        print("Best tour length: ", self.bestTourLength)
        print(self.bestTour)

def main():
    if len(sys.argv) != 3:
        print("./script.py <input> <output>")
        sys.exit()

    myAnt = AntTsp()
    try:
        myAnt.readData(sys.argv[1])
    except ValueError:
        print("lolpop ca marche po")

    print("Start")
    myAnt.solve()

main()
