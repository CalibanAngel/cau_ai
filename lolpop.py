#!/usr/bin/env python3

import random
import time
import sys
import math
from threading import Thread

g_timeDuration = 0

class city:
   distances = []
   neighbours = []

class OtpAlgo(Thread):

   def __init__(self, id, startTime, listCities):
      Thread.__init__(self)
      self.id = id
      self.distance = -1
      self.resultCities = []
      self.startTime = startTime
      self.listCities = listCities
      self.maxLen = len(listCities)

   def calcPathDistance(self, copyResultcity):
      res = 0
      for i in range(self.maxLen - 1):
         res += self.listCities[ copyResultcity[i] ].distances[ copyResultcity[i + 1] ]
      return res

   def optCalc(self, copyResultcity):
      loc = 0
      tabooValues = []
      tabooValues.append(0)
      while loc < self.maxLen - 1:
         before_dist = math.inf
         loc2 = 0
         res = -1

         currentCity = self.listCities[ copyResultcity[loc] ]

         while loc2 < 400:

            after_dist = currentCity.distances[ currentCity.neighbours[ loc2 ] ]
            if before_dist > after_dist and (currentCity.neighbours[ loc2 ] in tabooValues) == False:
               res = loc2
               before_dist = after_dist

            loc2 += 1

         if res != -1:
            tabooValues.append(currentCity.neighbours[ res ])
            pos = copyResultcity.index(currentCity.neighbours[ res ])
            value = copyResultcity[loc + 1]
            copyResultcity[loc + 1] = currentCity.neighbours[ res ]

            copyResultcity[ pos ] = value


         loc += 1
      return copyResultcity

   def run(self):
      while self.startTime + g_timeDuration > time.time():
         randResultcity = list(range(1,1000))
         random.shuffle(randResultcity)
         randResultcity.append(0)
         randResultcity.insert(0,0)

         tmpResultcity = self.optCalc(randResultcity)
         tmp_dist = self.calcPathDistance(tmpResultcity)
         if tmp_dist < self.distance or self.distance == -1:
            self.distance = tmp_dist
            self.resultCities = tmpResultcity

def getClosest(tab, lim):
   tabResult = []
   while (lim + 1) != 0:
      index = 0
      minValue = math.inf
      saveIndex = index
      while index < 1000:
         if (tab[index] < minValue and (index in tabResult) == False):
            minValue = tab[index]
            saveIndex = index
         index += 1
      tabResult.append(saveIndex)
      lim -= 1
   tabResult.pop(0)
   return tabResult

def loadDataFromFile(fileName):
   inputFile = open(fileName, 'r')
   listCities = []

   for line in inputFile:
      tmp = city()
      tmp.distances = list(map(int, line.split(",")))
      tmp.neighbours = getClosest(tmp.distances, 400)
      listCities.append(tmp)
   inputFile.close()

   return listCities

def main(argv):
   if len(argv) != 4:
      print ("./script.py <input> <output>")
      sys.exit()

   global g_timeDuration
   listCities = loadDataFromFile(argv[1])
   #for elem in listCities[0].neighbours:
   #   print(elem)
   g_timeDuration = int(argv[3])
   tabThread = []
   startTime = time.time()

   for threadId in range(8):
      tmpThread = OtpAlgo(threadId, startTime, listCities)
      tmpThread.start()
      tabThread.append( tmpThread )

   resultCities = []
   best_dist = -1
   for elem in tabThread:
      elem.join()
      if elem.distance < best_dist or best_dist == -1:
         best_dist = elem.distance
         resultCities = elem.resultCities

   print ("Best = " + str(best_dist))

   outputFile = open(argv[2], "w")
   for elem in resultCities:
      outputFile.write(str(elem + 1) + '\n')
   outputFile.close()

   print(str(time.time() - startTime))

main(sys.argv)
