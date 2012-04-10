#!/usr/bin/env python

# 
# LSST Data Management System
# Copyright 2008, 2009, 2010 LSST Corporation.
# 
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the LSST License Statement and 
# the GNU General Public License along with this program.  If not, 
# see <http://www.lsstcorp.org/LegalNotices/>.
#

# testAppInterface.py : A module with Python unittest code for testing
# functionality available through the appInterface module.  Currently
# only includes minimal fuzz testing and (unfinished) query replaying.

import MySQLdb as sql
import optparse
import time


class RunTests():

    def init(self, user, password, host, port, database):
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._dbName = database

    def connect2Db(self):
        print "Connecting to ", self._host, ":", self._port, \
              " as", self._user, "/", self._password, \
              "to db", self._dbName
        self._conn = sql.connect(user=self._user,
                                 passwd=self._password,
                                 host=self._host,
                                 port=int(self._port),
                                 db=self._dbName)
        self._cursor = self._conn.cursor()

    def runQuery(self, uniqueId):
        q1 = '''SELECT scisql_s2CPolyToBin(ra0, decl0, ra1, decl1, ra2, decl2, ra3, decl3) INTO @poly
                FROM Field 
                WHERE uniqueId = %s''' % uniqueId

        q2 = "CALL scisql.scisql_s2CPolyRegion(@poly, 20)"

        q3 = '''SELECT sourceId, ra, decl, htmId20 
                FROM   Source AS s 
                       INNER JOIN scisql.Region AS r ON (s.htmId20 BETWEEN r.htmMin AND r.htmMax) 
                WHERE  scisql_s2PtInCPoly(ra, decl, @poly) = 1'''

        self._runQuery(q1, False, uniqueId)
        self._runQuery(q2, False, uniqueId)
        self._runQuery(q3, True, uniqueId)

    def _runQuery(self, query, fetchResults, uniqueId):
        #print "Executing: ", query
        self._cursor.execute(query)
        if fetchResults:
            numRows = int(self._cursor.rowcount)
            print "Got", numRows, "rows for", uniqueId
            #if numRows > 0:
            #    rows = self._cursor.fetchall()
            #    print rows

    def tearDown(self):
        self._cursor.close()
        self._conn.close()


def main():
    op = optparse.OptionParser()
    op.add_option("-a", "--authFile", dest="authFile",
                  help='''File with mysql connection info. Format of one line:
 <token>:<value>. (Parsing is very basic so no extra spaces please.) Supported tokens:
host, port, user, pass.''')
    op.add_option("-d", "--db", dest="database",
                  help="database name")
    op.add_option("-i", "--interval", dest="interval",
                  default = 30,
                  help="Interval between queries")
    op.add_option("-f", "--from", dest="xFrom",
                  default = 1,
                  help="Beginning of the uniqueId range for the field")
    op.add_option("-t", "--to", dest="xTo",
                  default = 10,
                  help="End of the uniqueId range for the field")
    (_options, args) = op.parse_args()

    if _options.database is None:
        print "runTest.py: --database flag not set"
        print "Try `runTest.py --help` for more information."
        return -1

    ## read auth file
    if _options.authFile is None:
        print "runTest.py: --authFile flag not set"
        print "Try `runTest.py --help` for more information."
        return -1
    f = open(_options.authFile)
    for line in f:
        line = line.rstrip()
        (key, value) = line.split(':')
        if key == 'user':
            mysqlUser = value
        elif key == 'pass':
            mysqlPass = value
        elif key == 'host':
            mysqlHost = value
        elif key == 'port':
            mysqlPort = value
    f.close()

    x = RunTests()
    x.init(mysqlUser, mysqlPass, mysqlHost, mysqlPort, _options.database)
    x.connect2Db()

    counter = int(_options.xFrom)
    max = int(_options.xTo)
    while counter <= max:
        x.runQuery(counter)
        counter += 1
        time.sleep(int(_options.interval))

    x.tearDown()


if __name__ == '__main__':
    main()
