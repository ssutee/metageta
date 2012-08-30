# -*- coding: utf-8 -*-
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
batchuploadmef.py [options]
Options:
  -h, --help  show this help message and exit
  -d dir      The directory to search for MEF files
  -s site     Geonetwork site eg. http://someserver:8080
  -u user     Geonetwork username
  -p pass     Geonetwork password
  -r          Run recursively
'''
import os,sys
import urllib2, urllib, cookielib, fnmatch
import xml.dom.minidom as dom
try:from poster.encode import multipart_encode
except ImportError:
    print 'Error: unable to import the poster package.\nInstall it from http://atlee.ca/software/poster'
    sys.exit(1)

def main(site,username,password,directory,recurse):

    url='geonetwork/srv/en'

    handler=urllib2.HTTPHandler()
    proxy = urllib2.ProxyHandler({}) #This is so we avoid our proxy as urllib2 picks up the systemwide settings
    cj = cookielib.LWPCookieJar()

    #Login and get a cookie to use in the next call to the server
    service='xml.user.login'

    data = urllib.urlencode({'username':username,'password':password})
    request = urllib2.Request('%s/%s/%s?'%(site,url,service), data)
    opener = urllib2.build_opener(handler,proxy,urllib2.HTTPCookieProcessor(cj))
    try:
        result=dom.parseString(opener.open(request).read())
    except Exception,err:
        print err
        exit(1)
    try:
        assert(str(result.firstChild.localName) == 'ok')
    except:
        print 'Login failed!'
        exit(1)
    else:
        print 'Login successfull!'

        #Loop through the MEFs and upload them
        for mef in rglob(directory,'*.mef',recurse=recurse):
            uploadmef(mef,site,url,handler,proxy,cj)

def uploadmef(mef,site,url,handler,proxy,cj):
    #Set up the MEF import form values
    service='mef.import'
    formvalues={'insert_mode':'1',
              'file_type':'mef',
              'data':'',
              'template':'n',
              'title':'',
              'uuidAction':'overwrite',
              'styleSheet':'_none_',
              'group':'2',
              'category':'_none_'
              }

    print 'Uploading '+mef
    fo=open(mef,'rb')
    formvalues['mefFile']=fo
    datagen, headers = multipart_encode(formvalues)
    data=''
    for f in datagen:data+=f
    handler=urllib2.HTTPHandler()
    request = urllib2.Request('%s/%s/%s'%(site,url,service), data, headers)
    opener = urllib2.build_opener(handler,proxy,urllib2.HTTPCookieProcessor(cj))
    try:
        resultxml=opener.open(request).read()
        resultdom=dom.parseString(resultxml)
        assert(str(resultdom.firstChild.localName) in ['ok','id'])
    except Exception,err:
        print 'MEF upload failed!'
        print str(err)#resultxml
        exit(1)
    else:
        id=str(resultdom.firstChild.firstChild.data).strip(';')
        print 'Upload succeeded'
        print '%s/geonetwork/srv/en/metadata.show?id=%s&currTab=simple' % (site,id)
    fo.close()

class rglob:
    ''' A recursive glob adapted from
        os-path-walk-example-3.py - http://effbot.org/librarybook/os-path.htm
    '''
    def __init__(self, directory, pattern='*', recurse=False):
        self.stack = [directory]
        self.pattern = pattern
        self.files = []
        self.index = 0
        self.recurse = recurse

    def __getitem__(self, index):
        while 1:
            try:
                file = self.files[self.index]
                self.index = self.index + 1
            except IndexError:
                # pop next directory from stack
                self.directory = self.stack.pop()
                try:
                    self.files = os.listdir(self.directory)
                    self.index = 0
                except:pass
            else:
                # got a filename
                fullname = os.path.join(self.directory, file)
                if os.path.isdir(fullname) and self.recurse:
                    self.stack.append(fullname)
                if fnmatch.fnmatch(file, self.pattern):
                    return fullname

def exit(status=0):
    try:usr = raw_input("Press <Enter> to exit")
    except:pass
    sys.exit(status)

if __name__ == '__main__':

    import optparse
    description='Batch upload all MEF files in a directory to Geonetwork'
    parser = optparse.OptionParser(description=description)
    parser.add_option('-d', dest="directory", metavar="dir",
                      help='The directory to search for MEF files')
    parser.add_option("-s", dest="site", metavar="site",
                      help="Geonetwork site eg. http://someserver:8080")
    parser.add_option("-u", dest="username", metavar="user",
                      help="Geonetwork username")
    parser.add_option("-p", dest="password", metavar="pass",
                      help="Geonetwork password")
    opt=parser.add_option("-r", "--recurse", action="store_true", dest="recurse",default=False,
                      help="Search directory recursively")
    opts,args = parser.parse_args()
    kwargs={'recurse':opts.recurse}
    if not opts.site:
        try:kwargs['site'] = raw_input("Please enter the Geonetwork site eg. http://someserver:8080: ")
        except:pass
    else:kwargs['site']=opts.site
    if not opts.directory:
        try:kwargs['directory'] = raw_input("Please enter the MEF directory: ")
        except:pass
    else:kwargs['directory']=opts.directory
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

    if not 'site' in kwargs or not 'directory' in kwargs or not 'username' in kwargs or not 'password' in kwargs:
        print
        parser.print_help()
    else:
        main(**kwargs)

    try:usr = raw_input("Press <Enter> to exit")
    except:pass