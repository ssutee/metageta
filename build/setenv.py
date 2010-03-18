import os,sys

if __name__=='__main__':
    CURDIR=os.path.dirname(os.path.abspath(sys.argv[0]))
else:
    CURDIR=os.path.dirname(os.path.abspath(__file__))

PY_VER='Python26'
TOPDIR=os.path.dirname(CURDIR)
BIN_DIR=TOPDIR+'\\bin'
PY_DIR=BIN_DIR+'\\'+PY_VER #Don't mess with PYTHONHOME
DOWNLOAD_DIR=TOPDIR+'\\downloads'
del os  #Hide from autocomplete IDEs
del sys