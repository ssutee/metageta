"""Metadata driver for ESRI GRIDs"""
#list of file name regular expressions
format_regex=[r'hdr\.adf$']

#import base dataset modules
import __default__

# import other modules (use "_"  prefix to import privately)
import sys, os

class Dataset(__default__.Dataset): #Subclass of __default__.Dataset class so we get a load of metadata populated automatically,
                                    #normally we'd just subclass the base __dataset__.Dataset class
    """Read Metadata for a ESRI GRID dataset and reset the filename from <path?\hdr.adf to <path>"""
    def __init__(self,f):
        __default__.Dataset.__init__(self, f) #autopopulate basic metadata
        dir=os.path.dirname(f)
        self.metadata['filepath']=dir
        self.metadata['filename']=os.path.basename(dir)
        if self.metadata['compressiontype']=='Unknown':self.metadata['compressiontype']='RLE'
