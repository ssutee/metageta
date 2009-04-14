import logging,warnings
import threading
import Queue
from Tkinter import *

#Define some constants
DEBUG=logging.DEBUG
INFO=logging.INFO
WARNING=logging.WARNING
ERROR=logging.ERROR
CRITICAL=logging.CRITICAL
FATAL=logging.FATAL

class ProgressLogger(logging.Logger):
    """ Provide logger interface """

    def __init__(self,
               name,
               level=logging.INFO,
               format='%(asctime)s %(levelname)s %(message)s',
               dateformat='%H:%M:%S',
               logToConsole=False,
               logToFile=False,
               logToGUI=True,
               maxprogress=100,
               logfile=None,
               mode='w'):

        self.logToGUI=logToGUI

        ##Cos we've overwritten the class __init__ method        
        logging.Logger.__init__(self,name,level=level-1)#To handle the PROGRESS log records without them going to the console or file

        #Set up the handlers
        fmt = logging.Formatter(format, dateformat)
        
        if logToConsole:
           #create console handler and set level
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(fmt)
            self.addHandler(ch)

        if logToFile:
            #create file handler and set level
            if logfile:
                fh = logging.FileHandler(logfile, mode=mode)
                fh.setLevel(level)
                fh.setFormatter(fmt)
                self.addHandler(fh)

        if logToGUI:
            self.progress=0
            ph = ProgressLoggerHandler(name=name, maxprogress=maxprogress)

            #To handle the PROGRESS & END events without them going to the console or file
            logging.PROGRESS = level - 1
            logging.addLevelName(logging.PROGRESS, "PROGRESS") 
            ph.setLevel(logging.PROGRESS) 
            ph.setFormatter(fmt)
            self.addHandler(ph)

        #Handle warnings
        warnings.simplefilter('always')
        warnings.showwarning = self.showwarning

    def showwarning(self, msg, cat, fname, lno, file=None):
        self.warn(msg)

    def updateProgress(self,newMax=None):
        if self.logToGUI:self.log(logging.PROGRESS, newMax)

    def close(self):
        logging.shutdown()
 
class ProgressLoggerHandler(logging.Handler):
    """ Provide a Progress Bar Logging handler """

    def __init__(self, name=None, level=logging.INFO, maxprogress=100):
        """
        Initializes the instance - set up the Tkinter GUI and log output.
        """

        ##Cos we've overwritten the class __init__ method        
        logging.Handler.__init__(self)

        ##Create the log message queue and Shutdown event object
        self.queue  = Queue.Queue()
        self.event  = threading.Event() #Set to True during "logging.shutdown()" which calls "self.close()"
       
        ##Create the GUI
        self.gui=ProgressLoggerGUI(self.queue, self.event, name=name, maxprogress=maxprogress)
        self.gui.start()

    def emit(self, record):
        """ Process a event/log message """
        if record.levelname == 'PROGRESS':
            self.queue.put([record.levelname,record.getMessage()])
        else:
            self.queue.put([record.levelname, self.format(record)])

    def close(self):
        """
        Tidy up any resources used by the handler.
        """
        self.event.set()
        
class ProgressLoggerGUI(threading.Thread):
    """ Provide a Progress Bar Logging GUI """

    def __init__(self, queue, event, name=None, maxprogress=100):
        
        ##Cos we've overwritten the class __init__ method        
        threading.Thread.__init__(self)
        
        self.queue = queue
        self.event = event
        self.name = name
        self.maxprogress = maxprogress
        self.progress = 0

    def run(self):
        """
        Initializes the instance - set up the Tkinter progress bar and log output.
        """
        import ScrolledText

        self.master=Tk()
        self.master.title(self.name)
        self.master.geometry("600x800")
        
        """ Pack text message """
        Label(self.master, text='Progress', anchor=NW, justify=LEFT).pack(fill=X)

        """ Pack progress bar """
        self.progress_bar = ProgressBarView(self.master, max=self.maxprogress)
        self.progress_bar.pack(fill=X)

        """ Pack log window """
        self.logwnd = ScrolledText.ScrolledText(self.master, width=60, height=12, state=DISABLED)
        self.logwnd.pack(fill=BOTH, expand=1)

        """ Pack OK button """
        self.ok = Button(self.master, text="OK", width=10, command=self.onOk, state=DISABLED)
        self.ok.pack(side=RIGHT, padx=5, pady=5)

        #self.master.bind("<Return>", self.onOk)

        self.periodicCall()
        self.master.mainloop()

    def periodicCall(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                # Check contents of events queue
                event = self.queue.get(block=False)
                self.onEvent(event)
            except Queue.Empty:
                pass
                
        if self.event.isSet():
            self.ok.configure(state=ACTIVE)
        else:
            self.master.after(100, self.periodicCall)

    def onEvent(self, event):
        """ Process events """
        eventName = event[0]
        eventMsg  = event[1]
        if eventName == 'PROGRESS':
            max=eval(eventMsg)
            self.progress+=1
            self.progress_bar.updateProgress(self.progress, newMax=max)
            if self.progress>=max:self.ok.configure(state=ACTIVE)
        else:
            self.onLogMessage(eventMsg)

    def onLogMessage(self, msg):
        """ Display log message """
        w = self.logwnd
        w.configure(state=NORMAL)
        w.insert(END, msg)
        w.insert(END, "\n")
        w.see(END)
        w.configure(state=DISABLED)
        
    def onOk(self, event=None):
        self.master.withdraw()
        self.master.destroy()

class ProgressBarView:
  
  def __init__(self, master=None, orientation='horizontal',
      min=0, max=100, width=100, height=None,
      doLabel=1, appearance=None,
      fillColor=None, background=None,
      labelColor=None, labelFont=None,
      labelText='', labelFormat="%d%%",
      value=0.1, bd=2):
    # preserve various values
    self.master=master
    self.orientation=orientation
    self.min=min
    self.max=max
    self.doLabel=doLabel
    self.labelText=labelText
    self.labelFormat=labelFormat
    self.value=value
    if (fillColor == None) or (background == None) or (labelColor == None):
      # We have no system color names under linux. So use a workaround.
      #btn = Button(font=labelFont)
      btn = Button(master, text='0', font=labelFont)
      if fillColor == None:
        fillColor  = btn['foreground']
      if background == None:
        background = btn['disabledforeground']
      if labelColor == None:
        labelColor = btn['background']
    if height == None:
      l = Label(font=labelFont)
      height = l.winfo_reqheight()
    self.width      = width
    self.height     = height
    self.fillColor  = fillColor
    self.labelFont  = labelFont
    self.labelColor = labelColor
    self.background = background
    #
    # Create components
    #
    self.frame=Frame(master, relief=appearance, bd=bd, width=width, height=height)
    self.canvas=Canvas(self.frame, bd=0,
        highlightthickness=0, background=background, width=width, height=height)
    self.scale=self.canvas.create_rectangle(0, 0, width, height,
        fill=fillColor)
    self.label=self.canvas.create_text(width / 2, height / 2,
        text=labelText, anchor=CENTER, fill=labelColor, font=self.labelFont)
    self.canvas.pack(fill=BOTH)
    self.update()
    self.canvas.bind('<Configure>', self.onResize) # monitor size changes

  def onResize(self, event):
    if (self.width == event.width) and (self.height == event.height):
      return
    # Set new sizes
    self.width  = event.width
    self.height = event.height
    # Move label
    self.canvas.coords(self.label, event.width/2, event.height/2)
    # Display bar in new sizes
    self.update()

  def updateProgress(self, newValue, newMax=None):
    if newMax:
      self.max = newMax
    self.value = newValue
    self.update()

  def pack(self, *args, **kw):
    self.frame.pack(*args, **kw)

  def update(self):
    # Trim the values to be between min and max
    value=self.value
    if value > self.max:
      value = self.max
    if value < self.min:
      value = self.min
    # Adjust the rectangle
    if self.orientation == "horizontal":
      self.canvas.coords(self.scale, 0, 0,
          float(value) / self.max * self.width, self.height)
    else:
      self.canvas.coords(self.scale, 0,
          self.height - (float(value) / self.max*self.height),
          self.width, self.height)
    # And update the label
    if self.doLabel:
      if value:
        if value >= 0:
          pvalue = int((float(value) / float(self.max)) * 100.0)
        else:
          pvalue = 0
        self.canvas.itemconfig(self.label, text=self.labelFormat % pvalue)
      else:
        self.canvas.itemconfig(self.label, text='')
    else:
      self.canvas.itemconfig(self.label, text=self.labelFormat %
          self.labelText)
    self.canvas.update_idletasks()
