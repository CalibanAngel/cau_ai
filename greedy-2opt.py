#!/usr/bin/env python3

import random
import time
import sys
import copy

class city:
   lst = []
   visited = 0

listCities = []
Resultcity = []

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

def loop():
   pos = 0
   distance = 0
   closestCity = 0

   while allCitiesVisited(listCities) != True:
      listCities[pos].visited = 1
      closestCity = getMin(listCities[pos].lst)
      Resultcity.append(pos)
      distance += listCities[pos].lst[closestCity]
      pos = closestCity

   distance += listCities[pos].lst[0]
   Resultcity.append(listCities[pos].lst[0])
   return distance

def calcPathDistance(copyResultcity):
   res = 0
   for i in range(len(copyResultcity)):
      if i + 1 < len(copyResultcity):
         elem = copyResultcity[i]
         res += listCities[elem].lst[ copyResultcity[i + 1] ]
   return res

def optCalc():
   bestResultcity = []
   best_dist = -1

   for toc in range(1):
      copyResultcity = copy.deepcopy(Resultcity)
      loc = 0

      while loc < 999:
         before_dist = -1
         loc2 = 0
         res = 0

         while loc2 < 1000:
            after_dist = listCities[ copyResultcity[loc] ].lst[ copyResultcity[loc2] ]

            if before_dist == -1 or before_dist > after_dist:
               res = loc2
               before_dist = after_dist

            loc2 += 1

         if res != 0:
            tmp = copyResultcity[loc + 1]
            copyResultcity[loc + 1] = copyResultcity[res]
            copyResultcity[res] = tmp

         loc += 1

      temp_dist = calcPathDistance(copyResultcity)
      if temp_dist < best_dist or best_dist == -1:
         best_dist = temp_dist
         bestResultcity = copyResultcity

#   print("Distance opt = " + str(best_dist))
   return bestResultcity


def main(argv):
   if len(argv) != 3:
      sys.exit()
   inputFile = open(argv[1], 'r')
   outputFile = open(argv[2], 'w')
   for line in inputFile:
      tmp = city()
      tmp.lst = list(map(int, line.split(",") ))
      listCities.append(tmp)

   inputFile.close()

   startTime = time.time()
   res = loop()

#   print("Distance Greedy = " + str(res))
#   print(Resultcity)

   Resultcity = optCalc()

   for i in range(len(Resultcity)):
      elem = Resultcity[i]
      outputFile.write(str(elem + 1) + '\n')

   outputFile.close()

   print(str(time.time() - startTime))

main(sys.argv)
