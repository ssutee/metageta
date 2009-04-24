from glob import glob as _glob
import os.path as _path, re as _re, sys as _sys, imp as _imp
import __fields__
import utilities

#Private
__formats__={}

#Public
format_regex=[]
fields=__fields__.fields

debug=0
#Dynamically load all formats
for _lib in _glob(_path.join(__path__[0],'[a-z]*.py')):
    _lib=_path.splitext(_path.basename(_lib))[0]
    try:
      #import custom format and add to the list of formats
      #exec 'import %s' % _lib
      #__formats__[_lib]=eval(_lib)
      _f,_fn,_desc=_imp.find_module(_lib)
      __formats__[_lib]=_imp.load_module(_lib,_f,_fn,_desc)

      #append module _format_regex & fields to lists
      format_regex.extend([r for r in __formats__[_lib].format_regex if not r in format_regex])
    except:pass #TODO... warnings.warn etc...

#import generic formats (eg. GeoTiff, JP2, etc...)
import __default__
#append module _format_regex to list of format regexes
format_regex.extend([r for r in __default__.format_regex if not r in format_regex])

#def GetMetadata(f):
def Open(f):
    errors=[] #error stack

    #Try custom formats
    for lib in __formats__:
        fr='|'.join(__formats__[lib].format_regex)
        rx=_re.compile(fr, _re.IGNORECASE)
        if rx.search(f):
            try:
                ds=__formats__[lib].Dataset(f)
                return ds
            except NotImplementedError:
                pass #Used when a format driver can't open a file, but doesn't want to raise an error
            except Exception,err:
                if debug:
                    errinfo=utilities.FormatTraceback(_sys.exc_info()[2],debug)
                    errargs=[arg for arg in err.args]
                    errargs.append(errinfo)
                    err.args=tuple(errargs)
                errors.append(err)

    #Try default formats
    try:
        fr='|'.join(__default__.format_regex)
        rx=_re.compile(fr, _re.IGNORECASE)
        if rx.search(f):
            ds=__default__.Dataset(f)
            return ds
    except Exception,err:
        if debug:
            errinfo=utilities.FormatTraceback(_sys.exc_info()[2],debug)
            errargs=[arg for arg in err.args]
            errargs.append(errinfo)
            err.args=tuple(errargs)
        errors.append(err)

    #Couldn't open file, raise the last error in the stack
    #TODO... log the entire error stack
    if len(errors) > 0: raise errors[-1].__class__,'\n'.join(errors[-1].args)
    else:raise Exception, 'Unable to open %s' % f
