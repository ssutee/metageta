import os,sys,Tkinter,tkFileDialog
from icons import *

class GetArgs(object):
    '''Pop up a GUI dialog to gather arguments'''
    def __new__(self,*args):
        ##Initialise the class object
        self=object.__new__(self)
    #def __init__(self,*args):
        ''' Build and show a GUI dialog to collect arguments
            arg={'name'   :name, #
                 'type'   :type, #
                 'label'  :label, #
                 'default':default, #
                 'options':options
                }
        '''
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
            argtype=arg.argtype
            argname=arg.dest
            arg.lastdir=self._lastdir
            self._objs.append(argtype(self._root,i, arg))
            self._args[argname]=self._objs[i].value

        nargs=len(args)
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

class DirArg():
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
            var.set(ad)
            dir.set(ad)
            
class FileArg():
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
            var.set(fd)
            dir.set(os.path.split(fd)[0])

class BoolArg():
    def __init__(self,root,row,arg):
        self.value = Tkinter.BooleanVar()
        self.value.set(arg.default)
        TkLabel=Tkinter.Label(root, text=arg.help+':')
        TkCheckbutton=Tkinter.Checkbutton(root, variable=self.value)
        TkLabel.grid(row=row, column=0,sticky=Tkinter.W)
        TkCheckbutton.grid(row=row, column=1,sticky=Tkinter.W)

class Command:
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