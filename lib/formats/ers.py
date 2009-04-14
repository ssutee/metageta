#list of file name regular expressions
format_regex=[r'\.ers$']

#import base dataset modules
#import __dataset__
import __default__

# import other modules
import sys, os

class Dataset(__default__.Dataset): #Subclass of __default__.Dataset class so we get a load of metadata populated automatically,
                                    #normally we'd just subclass the base __dataset__.Dataset class
    """Read Metadata for a ERS image to ensure *.ers files get checked before tifs/etc... get passed to __default__.Dataset..."""
    def __init__(self,f):
        #Ignore ers's that reference certain data file formats
        ignore=['.ecw']
        dat=os.path.splitext(f)[0]
        if not os.path.exists(dat): #assume if a file with no extension exists, it is the ers data file
            ers=open(f).readlines()
            for line in ers:
                line=[part.strip() for part in line.split('=')]
                ext=''
                if line[0].upper() in ['SOURCEDATASET','DATAFILE']:
                    ext=os.path.splitext(line[1].strip('"'))[1]
                    break
            if ext in ignore:raise NotImplementedError #This error gets ignored in __init__.Open()
        __default__.Dataset.__init__(self, f) #autopopulate basic metadata
