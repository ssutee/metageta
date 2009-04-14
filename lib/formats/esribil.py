#list of file name regular expressions
format_regex=[r'\.hdr$',r'\.bil$',r'\.flt$']

#import base dataset modules
import __default__

# import other modules (use "_"  prefix to import privately)
import sys, os

class Dataset(__default__.Dataset): #Subclass of __default__.Dataset class so we get a load of metadata populated automatically,
                                    #normally we'd just subclass the base __dataset__.Dataset class
    """Read Metadata for a ESRI Bil image as GDAL doesn't work if you pass the header file..."""
    def __init__(self,f):
        ext=os.path.splitext(f)
        if ext[1].lower() == '.hdr': bil=r'%s.bil' % ext[0]
        else:bil=f
        if os.path.exists(bil):
            self.metadata['filepath']=bil
            self.metadata['filename']=os.path.split(bil)[1]
            __default__.Dataset.__init__(self, bil) #autopopulate basic metadata
            self.metadata['filepath']=bil
        else: raise NotImplementedError, '%s is not an ESRI bil file.' % f
