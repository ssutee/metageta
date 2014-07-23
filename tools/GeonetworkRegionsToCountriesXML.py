# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        GeonetworkRegionsToCountriesXML.py
# Purpose:     Generate country xml list for Geonetwork regions dropdown
#
# Author:      Luke Pinner, DSEWPaC
#
# Created:     07/02/2012
# Copyright:   (c) DSEWPaC 2012
# Licence:     MIT/X
#
# Usage: GeonetworkRegionsToCountriesXML.py [options] input_xls output_xls
#
#   Generate ANZLIC Geographic Descriptions for metadata crawl results using the
#   extent of place names in the standard ANZLIC
#   codelist:http://asdd.ga.gov.au/asdd/profileinfo/anzlic-allgens.xml
#
# Options:
#   -h, --help            show this help message and exit
#   -u user,     --user=user          User name.
#   -p password, --password=password  Password
#   -s sid,      --sid=sid            Oracle Database
#   -o output,   --output=output
#
#-------------------------------------------------------------------------------

import cx_Oracle
import os,sys,getpass

def main(user,password,sid,output):
    constr='%s/%s@%s'%(user,password,sid)
    con=cxConnection(constr)

    outfile=open(output,'w')
    outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    outfile.write('<countries>\n')
    for id,name in con.query('select IDDES, LABEL from REGIONSDES order by LABEL ASC'):
        outfile.write('    <country id="%s">%s</country>\n'%(id,name))
        print name
    outfile.write('</countries>')
    outfile.close()

class cxConnection(object):
    '''A simplified Connection object with query iterator and statement execution'''

    def __init__(self, conn_str,autocommit=False,arraysize=256):
        #Open and keep a connection. This is MUCH quicker than
        #opening one for every transaction/query...
        #Another other option is to create a SessionPool object which
        #allows for very fast connections to the database
        #where the same connection is being made multiple times
        self._con=cx_Oracle.connect(conn_str)

        #Does the user need to call .commit() after executing a transaction
        self._con.autocommit=autocommit

        #For tweaking query performance, implications for network bandwidth v. memory
        self.arraysize=arraysize

        #Make some of the Connection object methods available to the user
        self.commit=self._con.commit
        self.rollback=self._con.rollback

        #Open cursors
        self._cursors=[]

    def __del__(self):
        for cur in self._cursors:
            cur.close()
        self._con.close()
        del self._con


    def query(self,qry_str,arraysize=None):
        '''A simple query row generator'''
        cur = self._con.cursor()
        self._cursors.append(cur)
        if arraysize:cur.arraysize=arraysize
        else:cur.arraysize=self.arraysize
        result=cur.execute(qry_str)
        while True:
            try:
                rows=cur.fetchmany()
                if not rows:break
                for row in rows:yield row
            except:break
        #for row in result:  #Don't return the lot, i.e cur.fetchall(),
        #    yield row       #create a generator instead and close the
        cur.close()         #cursor when finished so the user doesn't have to.
        del self._cursors[self._cursors.index(cur)]
        del cur

    def execute(self,exc_str):
        '''A simple data manipulation method'''
        cur = self._con.cursor()
        self._cursors.append(cur)
        cur.execute(exc_str)
        result=cur.rowcount #How many rows were affected, can also be used as False/True (0/>0)
        cur.close()         #and to see if the statement was successfull
        del self._cursors[self._cursors.index(cur)]
        del cur
        return result

    def cursor(self):
        '''expose a cursor for more advanced stuff'''
        cur = self._con.cursor()
        self._cursors.append(cur)
        return cur

if __name__ == '__main__':
    import optparse #optparse deprecated in py2.7, will need to switch to argparse

    #Parse command line args
    description='Generate country xml list for Geonetwork regions dropdown'
    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(description=description,usage=usage)
    opt=parser.add_option("-u", "--user", dest="user", metavar="user", help="User name.")
    opt=parser.add_option("-p", "--password", dest="password", metavar="password",
        default=None, help="Password")
    opt=parser.add_option("-s", "--sid", dest="sid", metavar="sid",help="Database")
    opt=parser.add_option("-o", "--output", dest="output", metavar="output", help="User name.")

    optvals,argvals = parser.parse_args()
    if optvals.password is None:optvals.password=getpass.getpass('%s@%s password:'%(optvals.user,optvals.sid))
    main(optvals.user,optvals.password,optvals.sid,optvals.output)
