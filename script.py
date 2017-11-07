#!/usr/bin/env python3

import random
import time

tab = []

for line in open("/tmp/lolpop.txt", "r"):
   tab.append(list(map(int, line.split(",") )))

resDistance = -1
resCity = []

maxLen = len(tab)

startTime = time.time()

while time.time() - startTime < 28:

    distance = 0
    city = [ 0 ]

    currentPos = 0

    for i in range( maxLen - 1):
    
        while 1:
            pos = random.randint(0, maxLen - 1)
            if (pos in city) == False:
                break
        
        city.append(pos)
        distance += tab[currentPos][pos]
        currentPos = pos

    city.append(0)
    distance += tab[currentPos][0]

    if resDistance == -1 or distance < resDistance:
        resDistance = distance
        resCity = city
    
print(resCity)
print("Distance =", resDistance)
