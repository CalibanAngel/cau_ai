#!/usr/bin/env python3

import random
import time
import sys
from threading import Thread

g_timeDuration = 28

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
         res += self.listCities[ copyResultcity[i] ][ copyResultcity[i + 1] ]
      return res
   
   def optCalc(self, copyResultcity):
      loc = 0
      while loc < self.maxLen - 1:
         before_dist = -1
         loc2 = loc + 1
         res = 0

         while loc2 < self.maxLen:
            after_dist = self.listCities[ copyResultcity[loc] ][ copyResultcity[loc2] ]

            if before_dist == -1 or before_dist > after_dist:
               res = loc2
               before_dist = after_dist

            loc2 += 1

         if res != 0:
            tmp = copyResultcity[loc + 1]
            copyResultcity[loc + 1] = copyResultcity[res]
            copyResultcity[res] = tmp

         loc += 1
      return copyResultcity

   def run(self):   
      while self.startTime + g_timeDuration > time.time():
         randResultcity = []
         randResultcity.append(0)
         for i in range(1, 1000):
            while 1:
               randPos = random.randint(0, self.maxLen - 1)
               if (randPos in randResultcity) == False:
                  break
            randResultcity.append(randPos)
         randResultcity.append(0)

         tmpResultcity = self.optCalc(randResultcity)
         tmp_dist = self.calcPathDistance(tmpResultcity)
         if tmp_dist < self.distance or self.distance == -1:
            self.distance = tmp_dist
            self.resultCities = tmpResultcity


def loadDataFromFile(fileName):
   inputFile = open(fileName, 'r')
   listCities = []
   
   for line in inputFile:
      listCities.append( list(map(int, line.split(","))))
   inputFile.close()

   return listCities
   
def main(argv):
   if len(argv) != 3:
      print ("./script.py <input> <output>")
      sys.exit()

   listCities = loadDataFromFile(argv[1])

   tabThread = []
   startTime = time.time()

   for threadId in range(5):
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
      print("Thread: " + str(elem.id) + " => " + str(elem.distance))

   print ("Best = " + str(best_dist))
   print (resultCities)

   outputFile = open(argv[2], "w") 
   for elem in resultCities:
      outputFile.write(str(elem + 1) + '\n')
   outputFile.close()

   print(str(time.time() - startTime))

main(sys.argv)
