import threading
from Tkinter import *
class SplashScreen(threading.Thread):
    def __init__(self, imagefile=None, imagedata=None, timeout=0.001, callback=lambda:True):
        if not imagefile and not imagedata:raise Exception,'Image file name or base 64 encoded image data required!'
        if not timeout   and not callback: raise Exception,'Timeout (secs) or boolean callback function required!'

        self._root              = Tk()
        self._splash            = None

        if imagefile:self._image = PhotoImage(file=imagefile)
        else:        self._image = PhotoImage(data=imagedata)
        self._timeout  = timeout
        self._callback = callback

        threading.Thread.__init__ (self)
        self.start()
    def run(self):
        # Remove the app window from the display
        self._root.withdraw()

        # Calculate the geometry to center the splash image
        scrnWt = self._root.winfo_screenwidth()
        scrnHt = self._root.winfo_screenheight()

        imgWt = self._image.width()
        imgHt = self._image.height()

        imgXPos = (scrnWt / 2) - (imgWt / 2)
        imgYPos = (scrnHt / 2) - (imgHt / 2)

        self._root.overrideredirect(1)
        self._root.geometry('+%d+%d' % (imgXPos, imgYPos))
        Label(self._root, image=self._image, cursor='watch').pack()

        # Force Tk to draw the splash screen outside of mainloop()
        #self._splash.update()
        self._root.deiconify() # Become visible at the desired location
        self.__settimeout__()
        self._root.mainloop()

    def __settimeout__(self):
        self._root.after(int(self._timeout*1000),self.__poll__)
    def __poll__(self):
        if self._callback(): #If the callback function returns True
            self._root.destroy()
        else:
            self._root.after(int(self._timeout*1000),self.__poll__)

if __name__=='__main__':
    import time
    class callback:
        def __init__(self,value=False):
            self.value=value
        def check(self):
            #print 'I''ve been checked!'
            return self.value
    c=callback()
    splash=SplashScreen(imagefile=r'C:\WorkSpace\qlk.gif', callback=c.check)
    print 'Yawn... I''m going to sleep now!'
    time.sleep(5)
    print 'Stretch... I''m awake now!'
    c.value=True
    #SplashScreen(r'C:\WorkSpace\qlk.gif', timeout=5.0)

