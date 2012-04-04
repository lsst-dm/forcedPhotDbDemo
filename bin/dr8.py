#!/usr/bin/env python

import re
import sys
import forcedPhotDbDemo

def main(inName):
    obsList = forcedPhotDbDemo.observationsFromCsv(inName)
    count = 0
    for obs in obsList:
        if obs.stripe == 82:
            count += 1
    print count, len(obsList)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "USAGE: %s CSV_NAME" % sys.argv[0]
        exit(1)
    main(sys.argv[1])

