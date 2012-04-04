#!/usr/bin/env python

import math
import numpy.random

# Range in radians
raMin = 0
raMax = 360
decMin = math.degrees(-0.1)
decMax = math.degrees(0.15)

subaruDensity = 1000 / (2000*0.2/3600 * 4000*0.2/3600) # sources per square degree
totalNum = int((raMax - raMin) * (decMax - decMin) * subaruDensity)

numGroup = 100000

out = open("sources.csv", "w")
out.write("# id, raDeg, decDeg\n")
for group in range(totalNum // numGroup):
    start = group * numGroup
    index = numpy.arange(start, start + numGroup)
    ra = numpy.random.rand(numGroup) * (raMax - raMin) + raMin
    dec = numpy.random.rand(numGroup) * (decMax - decMin) + decMin
    for i, r, d in zip(index, ra, dec):
        out.write(",".join([str(value) for value in (i, r, d)]) + "\n")
    print group, "/", totalNum // numGroup
