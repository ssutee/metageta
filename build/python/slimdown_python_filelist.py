# -*- coding: latin-1 -*-
import glob,os,sys,zipfile as zip
sys.path.append('..')
import setenv,utilities

pylist='python_filelist.txt'
pywin='pythonwin' in sys.executable.lower()

prompt='''This will delete any *.py file from %s
if there is no matching file in %s.
Make sure you've run all tests before running this script.
Do you want to continue? Y/N [N]:'''

if pywin:
    ok=True
else:
    try:
        ok=raw_input(prompt%(setenv.PY_DIR,pylist))
    except:
        ok=''
    ok=len(ok)>0 and ok[0].upper() == 'Y'

if ok:
    bak='%s.backup.zip'%setenv.PY_DIR
    if os.path.exists(bak):os.remove(bak)
    bak=zip.ZipFile(bak,'w',zip.ZIP_DEFLATED)
    pylist=[l.strip() for l in open(pylist).readlines()]
    for f in utilities.rglob(setenv.PY_DIR,'*'):
        if os.path.isdir(f):
            if not os.listdir(f):
                #pass
                os.removedirs(f)
        else:
            if f[-3:] not in ['pyc','pyo']:
                n=f.replace(setenv.BIN_DIR+'\\','')
                if not n in pylist:
                    bak.write(f,n)
                    #os.remove(f)
    bak.close()
