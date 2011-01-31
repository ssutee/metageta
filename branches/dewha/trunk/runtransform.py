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
Metadata Transforms
===================
Script to run the Metadata Transforms.

Contains code to show GUI to gather input arguments when none are provided.
To run, call the eponymous batch file which sets the required environment variables.

Usage::
    runtransform.bat -x xls -t xsl -d dir

@newfield sysarg: Argument, Arguments
@sysarg: C{-x xls}: MS Excel spreadsheet to read from
@sysarg: C{-t xsl}: XSL transform - may be one of the pre-defined XSL transforms or a path to a custom XSL file.
@sysarg: C{-d dir}: Directory to write XML files to.

@note:B{Additional metadata elements}

      The ANZLIC ISO19139 stylesheet can make use of additional metadata elements that may be 
      manually added to the Excel spreadsheet and will be included in the output XML/MEF metadata.
      See the L{transforms} module documentation for more information.
 
@todo: Set up logging & debug properly.
'''

#Imports
import os,sys,glob
import Tkinter
import tkFileDialog
from Ft.Xml import Domlette as Dom
import utilities
import transforms
import progresslogger

def main(xls,xsl,dir,mef=False,cat='',log=None,debug=False,gui=False):
    '''
    Run the Metadata Transform
    @type  xls: C{str}
    @param xls: Excel spreadsheet to read metadata from
    @type  xsl: C{str}
    @param xsl: XSL transform {*.xsl|%s}
    @type  dir: C{str}
    @param dir: The directory to output metadata XML to
    @type  mef: C{boolean}
    @param mef: Create Metadata Exchange Format (MEF) file
    @type  cat: C{str}
    @param cat: The GeoNetwork category/ies to apply to the records ('|' separated)
    @type  log: C{boolean}
    @param log: Log file
    @type  debug: C{boolean}
    @param debug: Turn debug output on
    @type  gui: C{boolean}
    @param gui: Show the GUI progress dialog [Not yet implemented]

    @todo - start using the "-m" opt, currently not used at all.
          - add it to the GetArgs GUI
          - populate a dropdown list with transforms.categories
          - add a gui event that show/hides or enables/disables the categ list triggered by the mef opt
          - if <default> categ is selected, logic is:
            * check xls for categ column
            * if so use that,
            * if categ column is null for a row, of if no column at all then use default from config
          
    ''' % '|'.join(['"%s"'%s for s in transforms.transforms.keys()])
    if debug:level=progresslogger.DEBUG
    else:level=progresslogger.INFO
    windowicon=os.environ['CURDIR']+'/lib/wm_icon.ico'
    try:pl = progresslogger.ProgressLogger('Metadata Transforms', logToConsole=True, logToFile=False, logToGUI=False, level=level, windowicon=windowicon)
    except:pl = progresslogger.ProgressLogger('Metadata Transforms', logToConsole=True, logToFile=False, logToGUI=False, level=level)
    for rec in utilities.ExcelReader(xls, list):
        try:
            tmpcat=cat #dummy var as we may overwrite it
            overviews=[]
            deleted=False
            for i,val in enumerate(rec): #We use a list instead of a dict as there can be multiple fields with the same header/name
                if val[0]=='DELETED' and val[1] == 1:deleted=True
                elif val[0]=='filename':filename=val[1]
                elif val[0]=='guid':guid=val[1]
                elif val[0] in ['quicklook','thumbnail'] and val[1] != '':
                    overviews.append(val[1])
                elif val[0] == 'category' and val[1]:
                    tmpcat=val[1]
                    del rec[i]
            xmlfile='%s/%s.%s.xml'%(dir,filename,guid)
            meffile='%s/%s.%s.mef'%(dir,filename,guid)
            if deleted:
                pl.info('%s has been marked as deleted, XSLT processing will be terminated.'%filename)
                if os.path.exists(xmlfile):os.rename(xmlfile,'%s.deleted'%xmlfile)
                if os.path.exists(meffile):os.rename(meffile,'%s.deleted'%meffile)
                continue
            strxml=transforms.ListToXML(rec,'crawlresult')
            result = transforms.Transform(strxml, xsl, xmlfile)
            #if overviews:transforms.CreateMEF(dir,xmlfile,guid,overviews)
            #Create MEF even if there are no overviews
            if mef:transforms.CreateMEF(dir,xmlfile,guid,overviews,tmpcat)
            pl.info('Transformed metadata for ' +filename)
        except Exception,err:
            pl.error('%s\n%s' % (filename, utilities.ExceptionInfo()))
            pl.debug(utilities.ExceptionInfo(10))
            try:os.remove(xmlfile)
            except:pass
        
##    for rec in utilities.ExcelReader(xls):
##        try:
##            strxml=transforms.DictToXML(rec,'crawlresult')
##            result = transforms.Transform(strxml, xsl, '%s/%s.%s.xml'%(dir,rec['filename'],rec['guid']))
##            pl.info('Transformed metadata for ' +rec['filename'])
##        except Exception,err:
##            pl.error('%s\n%s' % (rec['filename'], utilities.ExceptionInfo()))
##            pl.debug(utilities.ExceptionInfo(10))


#========================================================================================================
if __name__ == '__main__':
    def mefcallback(mefarg,*args):
        checked=mefarg.value.get()
        for arg in args:
            arg.enabled=checked

    #To ensure uri's work...
    if os.path.basename(sys.argv[0])!=sys.argv[0]:os.chdir(os.path.dirname(sys.argv[0]))
    import optparse,icons,getargs
    
    APP='MetaGETA Transforms'
    ICON=icons.app_img
    description='Transform metadata to XML'

    parser = optparse.OptionParser(description=description)

    opt=parser.add_option("-x", dest="xls", metavar="xls", help="Excel spreadsheet")
    xlsarg=getargs.FileArg(opt,filter=[('Excel Spreadsheet','*.xls')],icon=icons.xls_img)
    xlsarg.tooltip="Excel spreadsheet to read metadata from."

    opt=parser.add_option('-d', dest="dir", metavar="dir", help='Output directory')
    opt.icon=icons.dir_img
    dirarg=getargs.DirArg(opt,initialdir='',enabled=True,icon=icons.dir_img)
    dirarg.tooltip='The directory to output metadata XML to.'
    
    opt=parser.add_option("-t", dest="xsl", metavar="xsl", help="XSL transform")
    xslarg=getargs.ComboBoxArg(opt,icon=icons.xsl_img)
    xslarg.tooltip="XSL transform {*.xsl|%s}." % '|'.join(['"%s"'%s for s in transforms.transforms.keys()])
    xslarg.options=transforms.transforms.keys()

    opt=parser.add_option("-m", action="store_true", dest="mef",default=False,
                     help="Create Metadata Exchange Format (MEF) file")
    mefarg=getargs.BoolArg(opt,icon=icons.xsl_img)
    mefarg.tooltip=opt.help+'?'

    opt=parser.add_option("-c", dest="cat", metavar="cat",default=transforms.categories['default'],   
                     help="Dataset category")
    catarg=getargs.ComboBoxArg(opt,enabled=False,multiselect=True,icon=icons.xsl_img)
    catarg.options=transforms.categories['categories']
    catarg.tooltip='Dataset category for Metadata Exchange Format (MEF) file. Default is "%s". If a "category" column exists in the spreadsheet, values from that column will override any selection here.'%transforms.categories['default']
    mefarg.callback=getargs.Command(mefcallback,mefarg,catarg)
    
    opt=parser.add_option("--debug", action="store_true", dest="debug",default=False, help="Turn debug output on")
    opt=parser.add_option("-l", dest="log", metavar="log",                            
                      help=optparse.SUPPRESS_HELP) #help="Log file")                     #Not yet implemented
    opt=parser.add_option("--gui", action="store_true", dest="gui", default=False,
                      help=optparse.SUPPRESS_HELP) #help="Show the GUI progress dialog") #Not yet implemented

    optvals,argvals = parser.parse_args()

    #Do we need to pop up the GUI?
    if not optvals.dir or not optvals.xls or not optvals.xsl:
        #Add existing command line args values to opt default values so they show in the gui
        for opt in parser.option_list:
            opt.default=vars(optvals).get(opt.dest,None)
        #Pop up the GUI
        args=getargs.GetArgs(xlsarg,dirarg,xslarg,mefarg,catarg,title=APP,icon=ICON)
        if args:#GetArgs returns None if user cancels the GUI
            main(args.xls,args.xsl,args.dir,args.mef,args.cat,optvals.log,optvals.gui,optvals.debug)
    else: #No need for the GUI
        main(optvals.xls,optvals.xsl,optvals.dir,optvals.mef,optvals.cat,optvals.log,optvals.gui,optvals.debug)
        