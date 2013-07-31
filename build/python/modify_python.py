import sys, os, shutil
sys.path.append('..')
sys.path.append(os.path.dirname(os.path.dirname(sys.argv[0])))
from setenv import *
from utilities import rglob

py_ver=PY_VER[-2:]
try:pythoncom  = utilities.rglob(os.environ['SYSTEMROOT'], 'pythoncom%s.dll'%py_ver)[0]
except:pythoncom=''
try:pywintypes = utilities.rglob(os.environ['SYSTEMROOT'], 'pywintypes%s.dll'%py_ver)[0]
except:pywintypes=''
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

raw_input('Press Enter to exit...')
