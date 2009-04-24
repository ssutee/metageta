import sys, os, re
from Tkinter import *
import tkFileDialog

import progresslogger
import formats
import geometry
import utilities

defaultgui=True #do we use the gui progress bar logger by default...?
defaultdebug=False #do we use debug logging by default...?

def main(dir,xls,shp,log, gui=defaultgui, debug=defaultdebug): 
    xls = utilities.checkExt(xls, ['.xls'])
    shp = utilities.checkExt(shp, ['.shp'])
    log = utilities.checkExt(shp, ['.log', '.txt'])

    format_regex  = formats.format_regex
    format_fields = formats.fields
    
    if debug:
        level=progresslogger.DEBUG
        formats.debug=debug
    else:level=progresslogger.INFO
    pl = progresslogger.ProgressLogger('Metadata Crawler',logfile=log, logToConsole=True, logToFile=True, logToGUI=gui, level=level)

    pl.debug('%s %s %s %s %s %s' % (dir,xls,shp,log,gui,debug))

    if os.path.exists(xls):
        try:
            os.remove(xls)
        except:
            pl.error('Unable to delete %s' % xls)
            pl.close()
            del pl
            sys.exit(1)

    ExcelWriter=utilities.ExcelWriter(xls,format_fields.keys())
    ShapeWriter=geometry.ShapeWriter(shp,format_fields,overwrite=True)

    cwd=os.curdir
    files=[]

    pl.info('Searching for files...')
    for f in utilities.rglob(dir,'|'.join(format_regex), True, re.IGNORECASE):files.append(f)
    files=utilities.fixSeparators(files)

    #Sort the files according to the priority of the regex formats
    filelist={}
    for f in files:
        i=0
        for r in format_regex:
            if re.search(r,f,re.IGNORECASE):
                if filelist.has_key(i):filelist[i].append(f)
                else:filelist[i]=[f]
            i+=1
    i=0
    files=[]
    for r in format_regex:
        if filelist.has_key(i):files.extend(filelist[i])
        i+=1

    i=0
    while len(files) > 0:
        f=files.pop(0)
        try:
            ds=formats.Open(f)
            md=ds.metadata
            geom=ds.extent
            
            pl.info('Extracted metadata from %s' % md['filepath'])
            for file in md['filelist'].split(','):
                if file in files:files.remove(file)
            md['filepath']=utilities.convertUNC(md['filepath'])
            md['filelist']=','.join([unc for unc in utilities.convertUNC(md['filelist'].split(','))])

            try:
                pass
                ExcelWriter.WriteRecord(md)
            except Exception,err:
               pl.error('%s\n%s' % (f, utilities.ExceptionInfo()))
               pl.debug(utilities.ExceptionInfo(int(debug)))
            try:
                ShapeWriter.WriteRecord(geom,md)
            except Exception,err:
                pl.error('%s\n%s' % (f, utilities.ExceptionInfo()))
                pl.debug(utilities.ExceptionInfo(int(debug)))

            i+=1
            pl.updateProgress(len(files)+i)
        except Exception,err:
           pl.error('%s\n%s' % (f, utilities.ExceptionInfo()))
           pl.debug(utilities.ExceptionInfo(int(debug)))
    if i == 0:
        pl.info("No data found")
    else:
        pl.info("Metadata extraction complete!")

    del pl
    #del ExcelWriter
    del ShapeWriter

#========================================================================================================
#Code below is for the GUI if run without arguments
#========================================================================================================
class Command:
    """ A class we can use to avoid using the tricky "Lambda" expression.
    "Python and Tkinter Programming" by John Grayson, introduces this idiom."""
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        apply(self.func, self.args, self.kwargs)
        

class GetArgs:
    def __init__(self):
        #base 64 encoded gif images for the GUI buttons
        shp_img = '''
            R0lGODlhEAAQAMIFABAQEIBnII+HgLS0pfDwsC8gIC8gIC8gICH5BAEKAAcALAAAAAAQABAAAAND
            eLrcJzBKqcQIN+MtwAvTNHTPSJwoQAigxwpouo4urZ7364I4cM8kC0x20n2GRGEtJGl9NFBMkBny
            HHzYrNbB7XoXCQA7'''

        dir_img='''
            R0lGODlhEAAQAMZUABAQEB8QEB8YEC8gIC8vIEA4ME9IQF9IIFpTSWBXQHBfUFBoj3NlRoBnII9v
            IIBwUGB3kH93YIZ5UZ94IJB/YIqAcLB/EI+IcICHn4+HgMCHEI6Oe4CPn4+PgMCQANCHEJ+PgICX
            r9CQANCQEJ+XgJKanaCgkK+fgJykoaKjo7CgkKimk+CfIKKoo6uoleCgMLCnkNCnUKuwpLSvkrSv
            mfCoMLWyn7+wkM+vcLS0pfCwML+4kPC3QNDAgM+/kPDAQP+/UODIgP/IUODQoP/QUPDQgP/QYP/P
            cPDYgP/XYP/XcP/YgPDgkP/ggP/gkPDnoP/noPDwoPDwsP/woP//////////////////////////
            ////////////////////////////////////////////////////////////////////////////
            /////////////////////////////////////////////////////////////////////////yH5
            BAEKAH8ALAAAAAAQABAAAAe1gH+Cg4SFhoQyHBghKIeEECV/ORwtEDYwmJg0hikLCzBDUlJTUCoz
            hZ4LKlGjUFBKJiQkIB0XgypPpFBLSb2+toImT643N5gnJ7IgIBkXJExQQTBN1NVNSkoxFc9OMDtK
            vkZEQjwvDC4gSNJNR0lGRkI/PDoNEn8gRTA+Su9CQPM1PhxY8SdDj2nw4umowWJEAwSCLqjAIaKi
            Bw0WLExwcGBDRAoRHihIYKAAgQECAARwxFJQIAA7'''
        xls_img='''
            R0lGODlhEAAQAPcAAAAAAIAAAACAAICAAAAAgIAAgACAgICAgMDAwP8AAAD/AP//AAAA//8A/wD/
            /////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMwAAZgAAmQAAzAAA/wAzAAAzMwAzZgAzmQAzzAAz/wBm
            AABmMwBmZgBmmQBmzABm/wCZAACZMwCZZgCZmQCZzACZ/wDMAADMMwDMZgDMmQDMzADM/wD/AAD/
            MwD/ZgD/mQD/zAD//zMAADMAMzMAZjMAmTMAzDMA/zMzADMzMzMzZjMzmTMzzDMz/zNmADNmMzNm
            ZjNmmTNmzDNm/zOZADOZMzOZZjOZmTOZzDOZ/zPMADPMMzPMZjPMmTPMzDPM/zP/ADP/MzP/ZjP/
            mTP/zDP//2YAAGYAM2YAZmYAmWYAzGYA/2YzAGYzM2YzZmYzmWYzzGYz/2ZmAGZmM2ZmZmZmmWZm
            zGZm/2aZAGaZM2aZZmaZmWaZzGaZ/2bMAGbMM2bMZmbMmWbMzGbM/2b/AGb/M2b/Zmb/mWb/zGb/
            /5kAAJkAM5kAZpkAmZkAzJkA/5kzAJkzM5kzZpkzmZkzzJkz/5lmAJlmM5lmZplmmZlmzJlm/5mZ
            AJmZM5mZZpmZmZmZzJmZ/5nMAJnMM5nMZpnMmZnMzJnM/5n/AJn/M5n/Zpn/mZn/zJn//8wAAMwA
            M8wAZswAmcwAzMwA/8wzAMwzM8wzZswzmcwzzMwz/8xmAMxmM8xmZsxmmcxmzMxm/8yZAMyZM8yZ
            ZsyZmcyZzMyZ/8zMAMzMM8zMZszMmczMzMzM/8z/AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8A
            mf8AzP8A//8zAP8zM/8zZv8zmf8zzP8z//9mAP9mM/9mZv9mmf9mzP9m//+ZAP+ZM/+ZZv+Zmf+Z
            zP+Z///MAP/MM//MZv/Mmf/MzP/M////AP//M///Zv//mf//zP///ywAAAAAEAAQAAAIngBfuUKF
            ipBBg4MS9umTJYsrBAheSZwokGBBhwgeaNzIUSOhLKgydhz5EdWrB4oOelT5kdDJLwgUKRpEKOUX
            Gtpannzw5ZVNQje15czicmNPg1lwCtW5EeirQV+IEtI2iOjOmh9dQc2SimqWQa4efGzYcGZUr4NQ
            ddSWimwWr33UahRKly61qn0Iza1rl9qXKVIPIkyY8Mtft4gTTwkIADs='''

        log_img='''
            R0lGODlhEAAQAIQQAG9s0oJ5eatyP6tycpePj6ulP6ulctWeOaulpdWentXSOcvHx9XS0v/MzP//
            zP///y8gIC8gIC8gIC8gIC8gIC8gIC8gIC8gIC8gIC8gIC8gIC8gIC8gIC8gIC8gIC8gICH5BAEK
            ABAALAAAAAAQABAAAAViICSOUNMwjEOOhyIUyhAbzMoAgJAQi9EjtRGAIXgUjw9CUDR8OJ9OJakJ
            fUqFjCSBZ11CqNWkt7ndLqLjbFg8zZa5bOw6znSfoVfm3clYIP5eEH4EAQFlCAsrEH2ICygoJCEA
            Ow=='''
        self.root = Tk()
        self.root.title('Metadata Crawler')

        last_dir = StringVar()
        last_dir.set('C:\\')

        dir_ico = PhotoImage(format='gif',data=dir_img)
        xls_ico = PhotoImage(format='gif',data=xls_img)
        shp_ico = PhotoImage(format='gif',data=shp_img)
        log_ico = PhotoImage(format='gif',data=log_img)
        sdir = StringVar()
        sxls = StringVar()
        sshp = StringVar()
        slog = StringVar()
        ldir=Label(self.root, text="Directory to search:")
        lxls=Label(self.root, text="Output spreadsheet:")
        lshp=Label(self.root, text="Output shapefile:")
        llog=Label(self.root, text="Output error log:")
        edir=Entry(self.root, textvariable=sdir)
        exls=Entry(self.root, textvariable=sxls)
        eshp=Entry(self.root, textvariable=sshp)
        elog=Entry(self.root, textvariable=slog)
        bdir = Button(self.root,image=dir_ico, command=Command(self.cmdDir, sdir,last_dir))
        bxls = Button(self.root,image=xls_ico, command=Command(self.cmdFile,sxls,[('Excel Spreadsheet','*.xls')],last_dir))
        bshp = Button(self.root,image=shp_ico, command=Command(self.cmdFile,sshp,[('ESRI Shapefile','*.shp')],last_dir))
        blog = Button(self.root,image=log_ico, command=Command(self.cmdFile,slog,[('Log File',('*.txt','*.log'))],last_dir))
        ldir.grid(row=0, column=0)
        lxls.grid(row=1, column=0)
        lshp.grid(row=2, column=0)
        llog.grid(row=3, column=0)
        edir.grid(row=0, column=1)
        exls.grid(row=1, column=1)
        eshp.grid(row=2, column=1)
        elog.grid(row=3, column=1)
        bdir.grid(row=0, column=2)
        bxls.grid(row=1, column=2)
        bshp.grid(row=2, column=2)
        blog.grid(row=3, column=2)

        bOK = Button(self.root,text="Ok", command=self.cmdOK)
        self.root.bind("<Return>", self.cmdOK)
        bOK.config(width=10)
        bCancel = Button(self.root,text="Cancel", command=self.cmdCancel)
        bOK.grid(row=4, column=1,sticky=E, padx=5,pady=5)
        bCancel.grid(row=4, column=2,sticky=E, pady=5)

        self.vars={'dir':sdir,'xls':sxls,'shp':sshp,'log':slog}
        
        self.root.mainloop()
        
    def cmdOK(self):
        ok,args=True,{}
        for var in self.vars:
            arg=self.vars[var].get()
            if arg=='':ok=False
            else:args[var]=arg
        if ok:
            self.root.destroy()
            main(**args)

    def cmdCancel(self):
        self.root.destroy()

    def cmdDir(self,var,dir):
        ad = tkFileDialog.askdirectory(parent=self.root,initialdir=dir.get(),title='Please select a directory to crawl for imagery')
        if ad:
            var.set(ad)
            dir.set(ad)

    def cmdFile(self,var,filter,dir):
        fd = tkFileDialog.asksaveasfilename(parent=self.root,filetypes=filter,initialdir=dir.get(),title='Please select a file')
        if fd:
            var.set(fd)
            dir.set(os.path.split(fd)[0])
            if os.path.exists(fd):
                try:os.remove(fd)
                except:
                    tkMessageBox.showerror(parent=self.root, title='Error', message='Unable to delete %s' % fd)
                    var.set('')
#========================================================================================================
#Above is for the GUI if run without arguments
#========================================================================================================
def StrToBool(val):
    if type(val) is str:
        if val =='True': return True
        if val =='False': return False
    else: return val
    
if __name__ == '__main__':
    if len(sys.argv) < 4:
        GetArgs() #Popup the gui
    else:
        args=sys.argv[1:]
        kwargs={'dir':args[0],
                'xls':args[1],
                'shp':args[2],
                'log':args[3]
        }
        if len(args) >= 5:
            kwargs['gui']=eval(args[4])
        if len(args) == 6:
            kwargs['debug']=eval(args[5])

        main(**kwargs)
        
