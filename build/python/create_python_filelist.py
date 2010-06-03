# -*- coding: latin-1 -*-
import os,sys,fnmatch
sys.path.append('..')
sys.path.append(os.path.dirname(os.path.dirname(sys.argv[0])))
import setenv,utilities

pylist=open('python_filelist.txt','w')

for f in sorted(utilities.rglob(setenv.PY_DIR, '*')):
    if not os.path.isdir(f) and not fnmatch.fnmatch(f,'*.py[c|o]'):
        print f
        pylist.write(f.replace(setenv.BIN_DIR+'\\','')+'\n')
pylist.close()
