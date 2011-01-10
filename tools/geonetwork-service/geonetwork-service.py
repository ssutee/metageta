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

import os,sys,time,subprocess,glob,ConfigParser,pythoncom,win32serviceutil,win32service,win32event,servicemanager,shutil

class AppServerSvc (win32serviceutil.ServiceFramework):
    _configfile_=os.path.splitext(os.path.abspath(__file__))[0]+'.ini'
    _svc_name_ = "geonetwork"
    _svc_display_name_ = "GeoNetwork OpenSource"
    _svc_description_ = "GeoNetwork is a catalog application to manage spatially referenced resources. It provides powerful metadata editing and search functions as well as an embedded interactive web map viewer."

    def __init__(self,args=None):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))

        config = ConfigParser.RawConfigParser()
        config.read(self._configfile_)

        self.geonetworkdir = config.get('defaults','geonetworkdir')
        self.geonetworkstart=config.get('defaults','geonetworkstart')
        self.geonetworkstop = config.get('defaults','geonetworkstop')

        self.start()

    def start(self):
        os.chdir(os.path.join(self.geonetworkdir, 'jetty'))
        interval=5
        rc=win32event.WaitForSingleObject(self.hWaitStop, interval)
        if rc==win32event.WAIT_TIMEOUT: # Start the service

            servicemanager.LogInfoMsg('Starting the %s service'%self._svc_display_name_)
            try:
                #Start GeoNetwork
                self.resetlogs()
                self.proc = subprocess.Popen(self.geonetworkstart, cwd=os.path.join(self.geonetworkdir, 'jetty'), shell=True)
            except Exception,err:
                servicemanager.LogErrorMsg('The %s service failed to start:\n%s'%(self._svc_display_name_,err))
                sys.exit(1)
            while True:
                rc=win32event.WaitForSingleObject(self.hWaitStop, interval)
                retcode=self.proc.poll()
                if retcode is not None:#GN has shutdown itself or crashed
                    servicemanager.LogErrorMsg('The %s service has stopped unexpectedly'%self._svc_display_name_)
                    break
                if rc==win32event.WAIT_OBJECT_0:# Stop the service
                    servicemanager.LogInfoMsg('Starting the %s service'%self._svc_display_name_)
                    self.stop()
                    break

    def stop(self):
        subprocess.Popen(self.geonetworkstop, cwd=os.path.join(self.geonetworkdir, 'jetty'), shell=True)
        for i in range(0,30):
            time.sleep(1)
            retcode=self.proc.poll()
            if retcode is not None:return
        #GN didn't shutdown in 30 secs, kill it.
        servicemanager.LogErrorMsg('The %s service failed to shutdown gracefully:\n%s'%(self._svc_display_name_,err))
        proc.kill()
        
    def resetlogs(self):
        self.unlink('logs/*request.log*')
        self.unlink('logs/output.log')
        self.move('logs/geonetwork.log.*', 'logs/archive/')
        self.move('logs/intermap.log.*', 'logs/archive/')
        self.move('logs/geoserver.log.*', 'logs/archive/')

    def move(self,pat,dir):
        for path in glob.iglob(pat):
            try:shutil.move(path, '%s/%s' % (dir,path))
            except:pass
    def unlink(self,pat):
        for path in glob.iglob(pat):
            try:os.unlink(path)
            except:pass

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
