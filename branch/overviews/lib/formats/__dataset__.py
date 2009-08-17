'''
Base Dataset class
==================
Defines the metadata fields and populates some basic info
'''

import utilities, uuid
import os,time
import UserDict 

#Import fieldnames
import __fields__

class Dataset(object):
    '''A base Dataset class'''
    def __new__(self,f):
        #Initialise the object
        self=object.__new__(self)

        #Initialise the fields & metadata properties
        self.fields=idict(__fields__.fields)#We don't want any fields added/deleted
        self._metadata={}
        for field in __fields__.fields:self._metadata[field]=''
        self._metadata=idict(self._metadata) #We don't want any fields added/deleted

        #Populate some basic fields
        self._metadata['filepath']=f

        return self

    def __classproperty__(fcn):
        try:return property( **fcn() )
        except:pass

    @__classproperty__
    def metadata():
        '''The metadata property.'''

        def fget(self):
            return self._metadata

        def fset(self, key, value):
            self._metadata[key] = value

        def fdel(self):pass

        return locals()


    def __init__(self,*args,**kwargs):
        pass #just in case a subclass tries to call this method

class idict(UserDict.IterableUserDict):
    '''The idict class. An immutable dictionary.
       modified from http://code.activestate.com/recipes/498072/
       to inherit UserDict.IterableUserDict
    '''

    def __setitem__(self, key, val):
        if key in self.data.keys():
            self.data[key]=val
        else:raise KeyError("Can't add keys")

    def __delitem__(self, key):
        raise KeyError("Can't delete keys")

    def pop(self, key):
        raise KeyError("Can't delete keys")
    def popitem(self):
        raise KeyError("Can't delete keys")