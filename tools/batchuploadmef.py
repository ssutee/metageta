def main(site,username,password,directory):
    import sys, urllib2, urllib, cookielib, glob
    import xml.dom.minidom as dom
    #Import multipart encode from the poster library - http://atlee.ca/software/poster
    from poster.encode import multipart_encode

    url='geonetwork/srv/en'

    handler=urllib2.HTTPHandler()
    proxy = urllib2.ProxyHandler({}) #This is so we avoid our proxy as urllib2 picks up the systemwide settings
    cj = cookielib.LWPCookieJar()

    #Login and get a cookie to use in the next call to the server
    service='xml.user.login'

    data = urllib.urlencode({'username':username,'password':password})
    request = urllib2.Request('http://%s/%s/%s?'%(site,url,service), data)
    opener = urllib2.build_opener(handler,proxy,urllib2.HTTPCookieProcessor(cj))
    result=dom.parseString(opener.open(request).read())
    try:
        result=dom.parseString(opener.open(request).read())
        assert(str(result.firstChild.localName) == 'ok')
    except:raise Exception, 'Login failed!'
    else:
        print 'Login successfull!'
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

        #Loop through the MEFs and upload them
        for mef in glob.glob('%s/*.mef'%directory):
            print 'Uploading '+mef
            fo=open(mef,'rb')   
            formvalues['mefFile']=fo
            datagen, headers = multipart_encode(formvalues)
            data=''
            for f in datagen:data+=f
            handler=urllib2.HTTPHandler()
            request = urllib2.Request('http://%s/%s/%s'%(site,url,service), data, headers)
            opener = urllib2.build_opener(handler,proxy,urllib2.HTTPCookieProcessor(cj))
            try:
                resultxml=opener.open(request).read()
                resultdom=dom.parseString(resultxml)
                assert(str(resultdom.firstChild.localName) in ['ok','id'])
            except:
                print 'MEF upload failed!'
                print resultxml
            else:
                id=str(resultdom.firstChild.firstChild.data).strip(';')
                print 'Upload succeeded'
                print 'http://%s/geonetwork/srv/en/metadata.show?id=%s&currTab=simple' % (site,id)
            fo.close()

if __name__ == '__main__':

    import optparse
    description='Batch upload all MEF files in a directory to Geonetwork'
    parser = optparse.OptionParser(description=description)
    parser.add_option('-d', dest="directory", metavar="dir",
                      help='The directory to search for MEF files')
    parser.add_option("-s", dest="site", metavar="site",
                      help="Geonetwork site eg. firefly:8080")
    parser.add_option("-u", dest="username", metavar="user",
                      help="Geonetwork username")
    parser.add_option("-p", dest="password", metavar="pass",
                      help="Geonetwork password")
    opts,args = parser.parse_args()
    kwargs={}
    if not opts.site:
        try:kwargs['site'] = raw_input("Please enter the Geonetwork site eg. firefly:8080: ")
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

    if not kwargs['site'] or not kwargs['directory'] or not kwargs['username'] or not kwargs['password']:
        print
        parser.print_help()
    else:
        main(**kwargs)
        
    try:usr = raw_input("Press <Enter> to exit")
    except:pass