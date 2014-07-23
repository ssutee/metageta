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
  -s site     Geonetwork site eg. http://pvac01mult01.internal.govt:8080
  -u user     Geonetwork username
  -p pass     Geonetwork password

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
    def __init__(self,site,username,password):

        self.username,self.password=username,password
        if site.startswith(('http://','https://')):
            self.url='%s/geonetwork/srv/en'%(site)
        else:
            self.url='http://%s/geonetwork/srv/en'%(site)

        self.loginservice='xml.user.login'
        self.searchservice='xml.search'
        self.delservice='metadata.delete'

        self.handler=urllib2.HTTPHandler()
        self.proxy = urllib2.ProxyHandler({}) #This is so we avoid our proxy as urllib2 picks up the systemwide settings

        #Login and get a cookie to use in the next call to the server
        data = urllib.urlencode({'username':username,'password':password})
        request = urllib2.Request('%s/%s'%(self.url,self.loginservice), data)
        self.opener = urllib2.build_opener(self.handler,self.proxy,urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
        try:
            result=etree.parse(self.opener.open(request))
            assert(result.getroot().tag == 'ok')
        except:
            raise RuntimeError('Login failed!')

        data=urllib.urlencode({'request':''})
        request = urllib2.Request('%s/%s'%(self.url,self.searchservice), data)
        result=etree.parse(self.opener.open(request))
        self.records=[e.text for e in result.findall('.//id')]
        if not self.records and len(result.findall('metadata'))>0:
            raise RuntimeError ('This script requires the "xml.metadata.get" "skipInfo" parameter to be set to "n" in config.xml')

    def delete(self,id):
        data=urllib.urlencode({'id':id})
        request = urllib2.Request('%s/%s'%(self.url,self.delservice), data)
        try:result=self.opener.open(request)
        except Exception as err:
            raise RuntimeError('Metadata delete failed!\n%s'%str(err))
        if result.code!=200:
            raise RuntimeError('%s: %s'%(result.code,result.read()))
        else:print '%s: %s'%(result.code,result.read())

def main(site,username,password, all=False):
    deleter = Deleter(site,username,password)
    for rec in deleter.records:
        print repr(rec)
        try:deleter.delete(rec)
        except Exception as err:
            print err

if __name__ == '__main__':
    import optparse

    description='Batch delete ALL records from Geonetwork'
    parser = optparse.OptionParser(description=description)
    parser.add_option("-s", dest="site", metavar="site",
                      help="Geonetwork site eg. http://pvac01mult01.internal.govt:8080")
    parser.add_option("-u", dest="username", metavar="user",
                      help="Geonetwork username")
    parser.add_option("-p", dest="password", metavar="pass",
                      help="Geonetwork password")
    opts,args = parser.parse_args()
    kwargs={}
    if not opts.site:
        try:kwargs['site'] = raw_input("Please enter the Geonetwork site eg. http://pvac01mult01.internal.govt:8080: ")
        except:pass
    else:kwargs['site']=opts.site
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

    if not kwargs['site'] or not kwargs['username'] or not kwargs['password']:
        print
        parser.print_help()
    else:
        main(**kwargs)

    try:usr = raw_input("Press <Enter> to exit")
    except:pass
