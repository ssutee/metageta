#Imports
import os,sys,StringIO,glob
#from lib.splashscreen import SplashScreen
#if len(sys.argv) == 1:SplashScreen(imagefile=r'C:\WorkSpace\qlk.gif', timeout=10)

from Tkinter import *
import tkFileDialog

from Ft.Xml.Xslt import Transform
from Ft.Xml import Parse
from Ft.Xml import Domlette as Dom
from lib import utilities

def main(xls,xsl,dir=''):
    for rec in utilities.ExcelReader(xls):
        doc=Dom.implementation.createRootNode('file:///%s.xml'%rec['guid'])
        docelement = doc.createElementNS(None, 'crawlresult')
        for col in rec:
            child=doc.createElementNS(None, col)
            text=doc.createTextNode(str(rec[col]))
            child.appendChild(text)
            docelement.appendChild(child)

        doc.appendChild(docelement)
        buf=StringIO.StringIO()
        Dom.Print(doc,stream=buf)
        if dir=='':
            result = Transform(buf.getvalue(), xsl, output=open('%s.xml'%rec['filepath'], 'w'))
        else:
            result = Transform(buf.getvalue(), 'xsl/'+xsl, output=open('%s/%s%s.xml'%(dir,rec['filename'],rec['guid']), 'w'))
        del buf

def GetTransforms():
    xslfiles={}
    for f in glob.glob('xsl/*.xml'):
        xml=Parse('file:%s'%f)
        name = str(xml.xpath('string(/stylesheet/@name)'))
        file = str(xml.xpath('string(/stylesheet/@file)'))
        xslfiles[name]=file
        #xslfiles.append({'name':name,'desc':desc,'file':file})
    return xslfiles
class Command:
    """ A class we can use to avoid using the tricky "Lambda" expression.
    "Python and Tkinter Programming" by John Grayson, introduces this idiom."""
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        apply(self.func, self.args, self.kwargs)
        

class DropList(Widget):
#class DropList(Widget):
    def __init__(self, root, options, stringvar, cnf={},**kwargs):
        self.root=root
        self.tk=root
        arrow=u'\u25bc'
        lbwidth=len(arrow)+2
        if kwargs.has_key('width'):
            fwidth=kwargs['width']
            ltwidth=fwidth-lbwidth
            self.width=fwidth
        else:
            ltwidth=max([len(o) for o in options])+4
            fwidth=ltwidth+lbwidth
            self.width=fwidth

        stringvar.set(options[0]) # default value

        self.frame=Frame(root,relief="sunken", bd=2,background='white')#,width=fwidth)
        self._lt=Label(self.frame,textvariable=stringvar, bd=0,relief="sunken",activebackground='white',background='white',width=ltwidth)
        self._lb=Label(self.frame,text=arrow,relief="raised", bd=2)
        self._m=Menu(root, tearoff=0,background='white')

        for o in options:
            self._m.add_command(label=o, command=Command(stringvar.set,o))

        # attach popup to canvas
        self._lt.bind("<Button-1>", self._popup)
        self._lt.grid(row=0, column=0)
        self._lb.bind("<Button-1>", self._popup)
        self._lb.grid(row=0, column=1)
        self.frame.pack()
    def _popup(self,event):
        self._m.post(self._lt.winfo_rootx(), self._lt.winfo_rooty())
    def pack(self, *args, **kw):
        self.frame.pack(*args, **kw)
    def grid(self, *args, **kw):
        self.frame.grid(*args, **kw)

class GetArgs:
    def __init__(self):
        #base 64 encoded gif images for the GUI buttons
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

        xsl_img='''
            R0lGODdhEAAQAOMPAAAAAAAAgAAAmQAA/zNmmQCAgDNm/zOZAIaGhjOZ/zPM/8DAwKbK8DP///Hx
            8f///ywBAAAADwAQAAAEWBDJSeW76Or9Vn4f5zzOAp5kOo5AC2QOMxaFQcrP+zDCUzyNROAhkL14
            pEJDcQiMijqkIXEYDIsOXWwU6N5Yn5VKpSWYz2fwRcwmldFo9bidhc3Hrrw+HwEAOw=='''
        
        self.root = Tk()
        self.root.title('Metadata Transform')
        self.root.withdraw()
        last_dir = StringVar()
        last_dir.set('C:\\')

        xls_ico = PhotoImage(format='gif',data=xls_img)
        xsl_ico = PhotoImage(format='gif',data=xsl_img)
        dir_ico = PhotoImage(format='gif',data=dir_img)

        sxls = StringVar()
        sxsl = StringVar()
        sdir = StringVar()

        lxls=Label(self.root, text="Input spreadsheet:")
        lxsl=Label(self.root, text="XSL Stylesheet:")
        ldir=Label(self.root, text="Output directory:")

        self.xslfiles=GetTransforms()
        options=self.xslfiles.keys()

        # exls=Entry(self.root, textvariable=sxls)
        # exsl=DropList(self.root,options,sxsl)
        # edir=Entry(self.root, textvariable=sdir)
        exsl=DropList(self.root,options,sxsl)
        exls=Entry(self.root, textvariable=sxls, width=exsl.width)
        edir=Entry(self.root, textvariable=sdir, width=exsl.width)

        bxls = Button(self.root,image=xls_ico, command=Command(self.cmdFile,sxls,[('Excel Spreadsheet','*.xls')],last_dir))
        bxsl = Label(self.root,image=xsl_ico)
        bdir = Button(self.root,image=dir_ico, command=Command(self.cmdDir, sdir,last_dir))

        lxls.grid(row=0, column=0, sticky=W)
        lxsl.grid(row=1, column=0, sticky=W)
        ldir.grid(row=2, column=0, sticky=W)

        exls.grid(row=0, column=1, sticky=W)
        exsl.grid(row=1, column=1, sticky=W)
        edir.grid(row=2, column=1, sticky=W)

        bxls.grid(row=0, column=2, sticky=E)
        bxsl.grid(row=1, column=2, sticky=E)
        bdir.grid(row=2, column=2, sticky=E)

        bOK = Button(self.root,text="Ok", command=self.cmdOK)
        self.root.bind("<Return>", self.cmdOK)
        bOK.config(width=10)
        bCancel = Button(self.root,text="Cancel", command=self.cmdCancel)
        bOK.grid(row=4, column=1,sticky=E, padx=5,pady=5)
        bCancel.grid(row=4, column=2,sticky=E, pady=5)

        self.vars={'dir':sdir,'xls':sxls,'xsl':sxsl}

        scrnWt = self.root.winfo_screenwidth()
        scrnHt = self.root.winfo_screenheight()

        imgWt = self.root.winfo_width()
        imgHt = self.root.winfo_height()

        imgXPos = (scrnWt / 2.0) - (imgWt / 2.0)
        imgYPos = (scrnHt / 2.0) - (imgHt / 2.0)

        self.root.overrideredirect(1)
        self.root.geometry('+%d+%d' % (imgXPos, imgYPos))
        
        self.root.update()
        self.root.mainloop()
        
    def cmdOK(self):
        ok,args=True,{}
        for var in self.vars:
            if var=='xsl':
                arg=self.xslfiles[self.vars[var].get()]
            else:
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
        fd = tkFileDialog.askopenfilename(parent=self.root,filetypes=filter,initialdir=dir.get(),title='Please select a file')
        if fd:
            var.set(fd)
            dir.set(os.path.split(fd)[0])
#========================================================================================================
#Above is for the GUI if run without arguments
#========================================================================================================

if __name__ == '__main__':
    if os.path.basename(sys.argv[0])!=sys.argv[0]:os.chdir(os.path.dirname(sys.argv[0]))
    args=sys.argv
    if len(args) < 3:
        GetArgs() #Popup the gui
    else:
        kwargs={'xls':args[1],
                'xsl':args[2]
        }
        if len(args) > 3:
            kwargs['dir']=args[3]
        if len(args) > 4:
            kwargs['gui']=eval(args[4])
        if len(args) > 5:
            kwargs['debug']=eval(args[5])

        main(**kwargs)
        