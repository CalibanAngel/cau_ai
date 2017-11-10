#!/usr/bin/env python3

import random
import time
import sys

class city:
   lst = []
   visited = 0
listCities = []
startTime = time.time()

if len(sys.argv) != 3:
   sys.exit()
inputFile = open(sys.argv[1], 'r')
outputFile = open(sys.argv[2], 'w')
for line in inputFile:
   tmp = city()
   tmp.lst = list(map(int, line.split(",") ))
   listCities.append(tmp)


distance = 0
Resultcity = []
pos = 0

closestCity = 0
def allCitiesVisited(tab):
   for elem in tab:
      if (elem.visited == 0):
         return False
   return True

def getMin(tab):
   ret = -1
   i = 0
   saveIndex = 0
   while i < len(tab):
      if ((ret == -1 or tab[i] < ret) and listCities[i].visited == 0):
         ret = tab[i]
         saveIndex = i
      i += 1
   return saveIndex
while allCitiesVisited(listCities) != True:
   oldPos = pos
   listCities[pos].visited = 1
   closestCity = getMin(listCities[pos].lst)
   Resultcity.append(pos + 1)
   distance += listCities[pos].lst[closestCity]
   pos = closestCity
distance += listCities[pos].lst[0]
Resultcity.append(listCities[pos].lst[0] + 1)
inputFile.close()
for elem in Resultcity:
   outputFile.write(str(elem) + '\n')
outputFile.close()
print(str(time.time() - startTime))
