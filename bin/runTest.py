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
                                 db=self._dbName)
        self._cursor = self._conn.cursor()

    def runQuery(self, query):
        self._cursor.execute(query)
        #rows = self._cursor.fetchall()

    def tearDown(self):
        self._cursor.close()
        self._conn.close()


def main():
    op = optparse.OptionParser()
    op.add_option("-a", "--authFile", dest="authFile",
                  help="File with mysql connection info")
    op.add_option("-d", "--db", dest="database",
                  help="database")
    op.add_option("-i", "--interval", dest="interval",
                  default = 30,
                  help="Interval between queries")
    op.add_option("-s", "--stopAfter", dest="stopAfter",
                  default = 10,
                  help="Stop after running STOPAFTER queries")
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

    counter = _options.stopAfter
    query = "SELECT COUNT(*) FROM Source"
    while counter > 0:
        x.runQuery(query)
        time.sleep(interval)

    x.tearDown()


if __name__ == '__main__':
    main()
