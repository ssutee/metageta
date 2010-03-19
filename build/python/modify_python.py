import sys, os, shutil
sys.path.append('..')
sys.path.append(os.path.dirname(os.path.dirname(sys.argv[0])))
from setenv import *
from utilities import rglob

py_ver=PY_VER[-2:]
try:pythoncom  = utilities.rglob(os.environ['SYSTEMROOT'], 'pythoncom%s.dll'%py_ver)[0]
except:pythoncom=''
try:pywintypes = utilities.rglob(os.environ['SYSTEMROOT'], 'pywintypes%s.dll'%py_ver)[0]
except:pythoncom=''
if pythoncom:
    src=pythoncom[0]
    dst=PY_DIR+'\\'+'pythoncom%s.dll'%py_ver
    if not os.path.exists(dst):
        try:shutil.copy(src,dst)
        except Exception,err:print err
if pywintypes:
    src=pywintypes[0]
    dst=PY_DIR+'\\'+'pywintypes%s.dll'%py_ver
    if not os.path.exists(dst):
        try:shutil.copy(src,dst)
        except Exception,err:print err

ft_config=PY_DIR+'\\Lib\\site-packages\\Ft\\__config__.py'
config_txt=open(ft_config).read()
src_txt=r"""    # standard distutils installation directories
    RESOURCEBUNDLE = False
    PYTHONLIBDIR   = 'C:\\%(PY_VER)s\\Lib\\site-packages\\'
    BINDIR         = 'C:\\%(PY_VER)s\\Scripts'
    DATADIR        = 'C:\\%(PY_VER)s\\Share\\4Suite'
    SYSCONFDIR     = 'C:\\%(PY_VER)s\\Share\\Settings\\4Suite'
    LOCALSTATEDIR  = 'C:\\%(PY_VER)s\\Share\\4Suite'
    LIBDIR         = 'C:\\%(PY_VER)s\\Share\\4Suite'
    LOCALEDIR      = 'C:\\%(PY_VER)s\\Share\\Locale'"""% {'PY_VER':PY_VER}
dst_txt=r"""    # standard distutils installation directories
    import os
    PYTHONHOME=os.environ['PYTHONHOME']
    RESOURCEBUNDLE = False
    PYTHONLIBDIR   = '%s\\Lib\\site-packages\\'%PYTHONHOME
    BINDIR         = '%s\\Scripts'%PYTHONHOME
    DATADIR        = '%s\\Share\\4Suite'%PYTHONHOME
    SYSCONFDIR     = '%s\\Share\\Settings\\4Suite'%PYTHONHOME
    LOCALSTATEDIR  = '%s\\Share\\4Suite'%PYTHONHOME
    LIBDIR         = '%s\\Share\\4Suite'%PYTHONHOME
    LOCALEDIR      = '%s\\Share\\Locale'%PYTHONHOME
    del os"""
if src_txt in config_txt:
    config_txt=config_txt.replace(src_txt,dst_txt)
    open(ft_config,'w').write(config_txt)
    
raw_input('Press Enter to exit...')
