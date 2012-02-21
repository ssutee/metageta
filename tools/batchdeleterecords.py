# -*- coding: latin-1 -*-
# Copyright (c) 2011 Australian Government, Department of Sustainability, Environment, Water, Population and Communities
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

'''
Usage:
batchdeleterecords.py [options]
Options:
  -h, --help  show this help message and exit
  -x xls      The crawler result spreadsheet containing images marked as deleted
  -s site     Geonetwork site eg. pandora:8079
  -u user     Geonetwork username
  -p pass     Geonetwork password
  --protocol  Protocol to connect to Geonetwork, default=http

Note: This script requires the "xml.metadata.get" "skipInfo" parameter to be set to "n"
in <GeoNetwork install dir>/web/geonetwork/WEB-INF/config.xml
		<service name="xml.metadata.get">
			<class name=".services.metadata.Show">
				<param name="skipPopularity" value="y" />
				<param name="skipInfo" value="n" /> <!--------Here --->
			</class>
		</service>

'''
import sys,warnings
import urllib2, urllib, cookielib
from lxml import etree
from metageta import utilities  as mgutils

class Deleter(object):
    def __init__(self,site,username,password, protocol):

        self.username,self.password=username,password
        self.url='%s://%s/geonetwork/srv/en'%(protocol,site)

        self.handler=urllib2.HTTPHandler()
        self.proxy = urllib2.ProxyHandler({}) #This is so we avoid our proxy as urllib2 picks up the systemwide settings

        #Login and get a cookie to use in the next call to the server
        service='xml.user.login'
        data = urllib.urlencode({'username':username,'password':password})
        request = urllib2.Request('%s/%s'%(self.url,service), data)
        self.opener = urllib2.build_opener(self.handler,self.proxy,urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
        try:
            result=etree.parse(self.opener.open(request))
            assert(result.getroot().tag == 'ok')
        except:
            raise RuntimeError('Login failed!')

    def delete(self,uid):
        getservice='xml.metadata.get'
        delservice='metadata.delete'
        data=urllib.urlencode({'uuid':uid})
        request = urllib2.Request('%s/%s'%(self.url,getservice), data)
        try:result=etree.parse(self.opener.open(request))
        except:raise RuntimeError ('Metadata not found - UUID %s'%uid)
        try:id=result.find('geonet:info/id',namespaces={'geonet':'http://www.fao.org/geonetwork'}).text
        except:raise RuntimeError ('This script requires the "xml.metadata.get" "skipInfo" parameter to be set to "n" in config.xml')
        data=urllib.urlencode({'id':id})
        request = urllib2.Request('%s/%s'%(self.url,delservice), data)
        try:result=self.opener.open(request)
        except Exception as err:
            print RuntimeError('Metadata delete failed!\n%s'%str(err))
        if result.code!=200:
            raise RuntimeError('%s: %s'%(result.code,result.read()))

def main(xls,site,username,password, protocol='http'):
    xlrdr = mgutils.ExcelReader(xls)
    deleter = Deleter(site,username,password, protocol)
    for rec in xlrdr:
        if rec.get('DELETED',0) in [1,'1']:
            try:deleter.delete(rec['guid'])
            except Exception as err:
                print err

if __name__ == '__main__':
    import optparse

    description='Batch delete crawl results marked as deleted from Geonetwork'
    parser = optparse.OptionParser(description=description)
    parser.add_option('-x', dest="xls", metavar="xls",
                      help='The crawler result spreadsheet containing images marked as deleted')
    parser.add_option("-s", dest="site", metavar="site",
                      help="Geonetwork site eg. pandora:8079")
    parser.add_option("-u", dest="username", metavar="user",
                      help="Geonetwork username")
    parser.add_option("-p", dest="password", metavar="pass",
                      help="Geonetwork password")
    parser.add_option("--protocol", dest="protocol", metavar="protocol",
                      help="Geonetwork password")
    opts,args = parser.parse_args()
    kwargs={}
    if not opts.site:
        try:kwargs['site'] = raw_input("Please enter the Geonetwork site eg. pandora:8079: ")
        except:pass
    else:kwargs['site']=opts.site
    if not opts.xls:
        try:kwargs['xls'] = raw_input("Please enter the crawl result XLS: ")
        except:pass
    else:kwargs['xls']=opts.xls
    if not opts.username:
        try:kwargs['username'] = raw_input("Please enter your Geonetwork username: ")
        except:pass
    else:kwargs['username']=opts.username
    if not opts.password:
        try:
            import getpass
            kwargs['password'] = getpass.getpass(prompt="Please enter your Geonetwork password: ")
        except:pass
    else:kwargs['password']=opts.password
    if opts.protocol:kwargs['protocol']=opts.protocol

    if not kwargs['site'] or not kwargs['xls'] or not kwargs['username'] or not kwargs['password']:
        print
        parser.print_help()
    else:
        main(**kwargs)

    try:usr = raw_input("Press <Enter> to exit")
    except:pass
