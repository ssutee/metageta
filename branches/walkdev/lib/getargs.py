# -*- coding: latin-1 -*-
# Copyright (c) 2009 Australian Government, Department of Environment, Heritage, Water and the Arts
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
Module to generate a GUI dialog to collect arguments
'''
import os,sys,Tkinter,tkFileDialog
from icons import *

class GetArgs(object):
    ''' Build and show a GUI dialog to collect arguments
        @type  args:    C{U{Option<http://docs.python.org/library/optparse.html>}}
        @param args:    One or more U{Option<http://docs.python.org/library/optparse.html>}s.
        
        @return:  C{None}

        @note:  The GetArgs class requires at least one additional custom attribute to be
                added to the optparse.Option. The required attribute is the argtype to use.
                Either L{DirArg}, L{FileArg} or L{BoolArg}.  L{DirArg} and L{FileArg} also require
                additional custom attributes.

                Example::
                        parser = optparse.OptionParser(description=description)
                        opt=parser.add_option('-d', dest="dir", metavar="dir",help='The directory to crawl')
                        opt.icon=icons.dir_img      #Custom icon and argtype attributes
                        opt.argtype=getargs.DirArg
                        
                        opt=parser.add_option("-u", "--update", action="store_true", dest="update",default=False,
                                          help="Update existing spreadsheet")
                        opt.argtype=getargs.BoolArg #Custom argtype attribute

                        opt=parser.add_option("-l", dest="log", metavar="log",help="Log file")
                        opt.argtype=getargs.FileArg #Custom argtype, icon and filter attributes
                        opt.icon=icons.log_img
                        opt.filter=[('Log File',('*.txt','*.log'))]

                        #Parse existing command line args
                        optvals,argvals = parser.parse_args()
                        #Pop up the GUI
                        args=getargs.GetArgs(*parser.option_list)

            @see: L{runcrawler} for a more complete example.                  
    '''
    def __new__(self,*args):
        self=object.__new__(self)
        title='MetaGETA'
        icon=os.environ['CURDIR']+'/lib/wm_icon.ico'
        windowicon=icon

        self._root = Tkinter.Tk()
        self._root.title(title)
        try:self._root.wm_iconbitmap(windowicon)
        except:pass

        # Calculate the geometry to centre the app
        scrnWt = self._root.winfo_screenwidth()
        scrnHt = self._root.winfo_screenheight()
        appWt = self._root.winfo_width()
        appHt = self._root.winfo_height()
        appXPos = (scrnWt / 2) - (appWt / 2)
        appYPos = (scrnHt / 2) - (appHt / 2)
        self._root.geometry('+%d+%d' % (appXPos, appYPos))
        
        self._lastdir = Tkinter.StringVar()
        self._lastdir.set('')

        self._args={}
        self._objs=[]
        for i,arg in enumerate(args):
            if 'argtype' in vars(arg):
                argtype=arg.argtype
                argname=arg.dest
                arg.lastdir=self._lastdir
                self._objs.append(argtype(self._root,i, arg))
                self._args[argname]=self._objs[i].value

        nargs=len(self._objs)
        self._root.bind("<Return>", self._cmdok)
        TkFrame=Tkinter.Frame(self._root)
        TkFrame.grid(row=nargs,columnspan=3,sticky=Tkinter.E)
        bOK = Tkinter.Button(TkFrame,text="Ok", command=self._cmdok)
        bOK.config(width=8)
        bOK.grid(row=0, column=1,sticky=Tkinter.E, padx=5,pady=5)
        bCancel = Tkinter.Button(TkFrame,text="Cancel", command=self._cmdcancel)
        bCancel.config(width=8)
        bCancel.grid(row=0, column=2,sticky=Tkinter.E, padx=5,pady=5)
        self._cancelled = False

        self._root.mainloop()
        if self._cancelled:return None
        else:return self

    def _cmdok(self,*args,**kwargs):
        ok=True
        for arg in self._args:
            try:vars(self)[arg]=self._args[arg].get()
            except:pass            
            if vars(self)[arg]=='':
                ok=False
                break
        if ok:
            self._root.destroy()

    def _cmdcancel(self):
        self._root.destroy()
        self._cancelled =True

class DirArg(object):
    ''' Build a directory browser 

        @type  root: C{Tkinter.Tk}
        @param root: Root Tk instance.
        @type  row:  C{int}
        @param row:  Grid row to place the directory browser in.
        @type  arg:  C{U{Option<http://docs.python.org/library/optparse.html>}}
        @param arg:  An U{Option<http://docs.python.org/library/optparse.html>}.
        
        @note:  The DirArg class requires an additional custom attribute to be
                added to the optparse.Option. This is the L{icon<icons>} to display on the button.

                Example::
                        parser = optparse.OptionParser(description=description)
                        opt=parser.add_option('-d', dest="dir", metavar="dir",help='The directory to crawl')
                        opt.argtype=getargs.DirArg
                        opt.icon=icons.dir_img
    '''
    def __init__(self,root,row,arg):
        self.TkPhotoImage = Tkinter.PhotoImage(format=arg.icon.format,data=arg.icon.data) # keep a reference! See http://effbot.org/tkinterbook/photoimage.htm
        self.value = Tkinter.StringVar()
        if arg.default is not None:self.value.set(arg.default)
        TkLabel=Tkinter.Label(root, text=arg.help+':')
        TkEntry=Tkinter.Entry(root, textvariable=self.value)
        TkButton = Tkinter.Button(root,image=self.TkPhotoImage, command=Command(self.cmd,root,arg.help,arg.lastdir,self.value))
        TkLabel.grid(row=row, column=0,sticky=Tkinter.W, padx=2)
        TkEntry.grid(row=row, column=1,sticky=Tkinter.E+Tkinter.W, padx=2)
        TkButton.grid(row=row, column=2,sticky=Tkinter.E, padx=2)
        
    def cmd(self,root,label,dir,var):
        ad = tkFileDialog.askdirectory(parent=root,initialdir=dir.get(),title=label)
        if ad:
            ad=os.path.normpath(ad)
            var.set(ad)
            dir.set(ad)
            
class FileArg(object):
    ''' Build a file browser 

        @type  root: C{Tkinter.Tk}
        @param root: Root Tk instance.
        @type  row:  C{int}
        @param row:  Grid row to place the file browser in.
        @type  arg:  C{U{Option<http://docs.python.org/library/optparse.html>}}
        @param arg:  An U{Option<http://docs.python.org/library/optparse.html>}.
        
        @note:  The FileArg class requires two additional custom attributes to be
                added to the optparse.Option. These are the L{icon<icons>} to display on the button
                and filter in U{tkFileDialog.askopenfilename<http://tkinter.unpythonic.net/wiki/tkFileDialog>}
                filetypes format.

                Example::
                    opt=parser.add_option("-l", dest="log", metavar="log",help="Log file")
                    opt.argtype=getargs.FileArg
                    opt.icon=icons.log_img
                    opt.filter=[('Log File',('*.txt','*.log'))]
    '''
    def __init__(self,root,row,arg):
        self.TkPhotoImage = Tkinter.PhotoImage(format=arg.icon.format,data=arg.icon.data) # keep a reference! See http://effbot.org/tkinterbook/photoimage.htm
        self.value = Tkinter.StringVar()
        if arg.default is not None:self.value.set(arg.default)
        TkLabel=Tkinter.Label(root, text=arg.help+':')
        TkEntry=Tkinter.Entry(root, textvariable=self.value)
        TkButton = Tkinter.Button(root,image=self.TkPhotoImage,command=Command(self.cmd,root,arg.help,arg.filter,arg.lastdir,self.value))
        TkLabel.grid(row=row, column=0,sticky=Tkinter.W, padx=2)
        TkEntry.grid(row=row, column=1,sticky=Tkinter.E+Tkinter.W, padx=2)
        TkButton.grid(row=row, column=2,sticky=Tkinter.E, padx=2)
        
    def cmd(self,root,label,filter,dir,var):
        if sys.platform[0:3].lower()=='win':
            ##Win32 GUI hack to avoid "<somefile> exists. Do you want to replace it?"
            ##when using tkFileDialog.asksaveasfilename
            import win32gui
            #Convert filter from [('Python Scripts',('*.py','*.pyw')),('Text files','*.txt')] format
            #to 'Python Scripts\0*.py;*.pyw\0Text files\0*.txt\0' format
            winfilter=''
            for desc,ext in filter:
                if type(ext) in [list,tuple]:ext=';'.join(ext)
                winfilter+='%s (%s)\0%s\0'%(desc,ext,ext)
            try:
                fd, filter, flags=win32gui.GetSaveFileNameW(
                    InitialDir=dir.get(),
                    Title='Please select a file',
                    Filter=winfilter)
            except:fd=None
        else:
            fd = tkFileDialog.asksaveasfilename(parent=root,filetypes=filter,initialdir=dir.get(),title=label)
        if fd:
            fd=os.path.normpath(fd)
            var.set(fd)
            dir.set(os.path.split(fd)[0])

class BoolArg(object):
    ''' Build a boolean checkbox 

        @type  root: C{Tkinter.Tk}
        @param root: Root Tk instance.
        @type  row:  C{int}
        @param row:  Grid row to place the checkbox in.
        @type  arg:  C{U{Option<http://docs.python.org/library/optparse.html>}}
        @param arg:  An U{Option<http://docs.python.org/library/optparse.html>}.
    '''
    def __init__(self,root,row,arg):
        self.value = Tkinter.BooleanVar()
        self.value.set(arg.default)
        TkLabel=Tkinter.Label(root, text=arg.help+':')
        TkCheckbutton=Tkinter.Checkbutton(root, variable=self.value)
        TkLabel.grid(row=row, column=0,sticky=Tkinter.W)
        TkCheckbutton.grid(row=row, column=1,sticky=Tkinter.W)

class Command(object):
    """ A class we can use to avoid using the tricky "Lambda" expression.
    "Python and Tkinter Programming" by John Grayson, introduces this idiom."""
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        apply(self.func, self.args, self.kwargs)
        

if __name__ == '__main__':
    import optparse,icons,getargs
    reload(getargs)
    description='Run the metadata crawler'
    parser = optparse.OptionParser(description=description)
    opt=parser.add_option('-d', dest="dir", metavar="dir",help='The directory to crawl')
    opt.icon=icons.dir_img
    opt.argtype=getargs.DirArg
    
    opt=parser.add_option("-x", dest="xls", metavar="xls",help="Output Excel spreadsheet")
    opt.argtype=getargs.FileArg
    opt.icon=icons.xls_img
    opt.filter=[('Excel Spreadsheet','*.xls')]

    opt=parser.add_option("-s", dest="shp", metavar="shp",help="Output shapefile")
    opt.argtype=getargs.FileArg
    opt.icon=icons.shp_img
    opt.filter=[('ESRI Shapefile','*.shp')]

    opt=parser.add_option("-l", dest="log", metavar="log",help="Log file")
    opt.argtype=getargs.FileArg
    opt.icon=icons.log_img
    opt.filter=[('Log File',('*.txt','*.log'))]
    
    opt=parser.add_option("-o", action="store_true", dest="ovs",default=False,
                      help="Generate overview images")
    #opt.argtype=getargs.BoolArg
    opt=parser.add_option("--nomd", action="store_true", dest="nomd",default=False,
                      help="Get basic file info only")
    opt.argtype=getargs.BoolArg
    opt=parser.add_option("--debug", action="store_true", dest="debug",default=False,
                      help="Turn debug output on")
    opt=parser.add_option("--gui", action="store_true", dest="gui", default=False,
                      help="Show the GUI progress dialog")
    optvals,argvals = parser.parse_args()
    for opt in parser.option_list:
        if 'argtype' in vars(opt):
            opt.default=vars(optvals)[opt.dest]
    if not optvals.dir or not optvals.log or not optvals.shp or not optvals.xls:
        args=getargs.GetArgs(*[opt for opt in parser.option_list if 'argtype' in vars(opt)])