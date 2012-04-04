#!/usr/bin/env python

import re
import math

class Observation(object):
    def __init__(self, skyVersion, run, stripe, strip, camcol, field, quality, node, incl,
                 muStart, muEnd, nuStart, nuEnd,
                 degrees=True):
        self.skyVersion = int(skyVersion)
        self.run = int(run)
        self.stripe = int(stripe)
        self.strip = strip
        self.camcol = int(camcol)
        self.field = int(field)
        self.quality = int(quality)
        self.node = float(node)
        self.incl = float(incl)
        self.muStart = float(muStart)
        self.muEnd = float(muEnd)
        self.nuStart = float(nuStart)
        self.nuEnd = float(nuEnd)
        self.width = 2048
        self.height = 1361
        if degrees:
            self.convertFromDegrees()

    def convertFromDegrees(self):
        for name in ('node', 'incl', 'muStart', 'muEnd', 'nuStart', 'nuEnd'):
            setattr(self, name, math.radians(getattr(self, name)))

    def __str__(self):
        return "skyVersion=%s run=%d stripe=%d strip=%s camcol=%d field=%d node=%f incl=%f mu=%f--%f nu=%f--%f" % \
              (self.skyVersion, self.run, self.stripe, self.strip, self.camcol, self.field,
               self.node, self.incl, self.muStart, self.muEnd, self.nuStart, self.nuEnd)

    def radecAvg(self):
        muAvg, nuAvg = 0.0, 0.0
        for mu, nu in [(self.muStart, self.nuStart),
                       (self.muEnd, self.nuStart),
                       (self.muEnd, self.nuEnd),
                       (self.muStart, self.nuEnd)]:
            muAvg += mu
            nuAvg += nu
        muAvg /= 4.0
        nuAvg /= 4.0
        return sdss2radec(self.node, self.incl, muAvg, nuAvg)


    def name(self):
        return "Stripe %d, Field %d" % (self.stripe, self.field)


def sdss2radec(node, incl, mu, nu):
    muNode = mu - node

    x2 = math.cos(muNode)*math.cos(nu)
    y2 = math.sin(muNode)*math.cos(nu)
    z2 = math.sin(nu)
    y1 = y2*math.cos(incl) - z2*math.sin(incl)
    z1 = y2*math.sin(incl) + z2*math.cos(incl)

    ra = math.atan2(y1, x2) + node
    dec = math.asin(z1)
    return ra, dec

def observationsFromCsv(csvName):
    csv = open(csvName)
    csv.readline()                  # Heading line
    obs = []
    for line in csv:
        data = re.split(r",", line.rstrip())
        obs.append(Observation(*data))
    return obs
