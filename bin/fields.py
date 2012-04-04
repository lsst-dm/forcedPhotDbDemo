#!/usr/bin/env python

import re
import sys
import math
import forcedPhotDbDemo

import collections

def main(inName, outName):
    obsList = forcedPhotDbDemo.observationsFromCsv(inName)

    out = open(outName, "w")
    out.write("# run, field, raDeg0, decDeg0, raDeg1, decDeg1, raDeg2, decDeg2, raDeg3, decDeg3\n")
    for obs in obsList:
        output = [obs.run, obs.field]
        for mu, nu in ((obs.muStart, obs.nuStart),
                       (obs.muStart, obs.nuEnd),
                       (obs.muEnd,   obs.nuEnd),
                       (obs.muEnd,   obs.nuStart)):
            ra,dec = forcedPhotDbDemo.sdss2radec(obs.node, obs.incl, mu, nu)
            output.append(ra)
            output.append(dec)
        out.write(",".join([str(value) for value in output]) + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "USAGE: %s SDSS_NAME OUTPUT_NAME" % sys.argv[0]
        exit(1)
    main(sys.argv[1], sys.argv[2])

