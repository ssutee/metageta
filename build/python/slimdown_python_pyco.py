# -*- coding: latin-1 -*-
import glob,os,sys,zipfile as zip
sys.path.append('..')
sys.path.append(os.path.dirname(os.path.dirname(sys.argv[0])))
import setenv,utilities

prompt='''This will delete any *.py file from %s
if there is no related *.py[c|o] file.
Make sure you've run all tests before running this script.
Do you want to continue? Y/N [N]:'''
try:
    ok=raw_input(prompt%setenv.PY_DIR)
except:
    ok=''

if len(ok)>0 and ok[0].upper() == 'Y':
    bak='%s.backup.zip'%setenv.PY_DIR
    if os.path.exists(bak):os.remove(bak)
    bak=zip.ZipFile(bak,'w',zip.ZIP_DEFLATED)
    for py in utilities.rglob(setenv.PY_DIR, '*.py'):
        if not glob.glob(py+'[c|o]') and 'pythonwin' not in py:
            bak.write(py,py.replace(setenv.BIN_DIR,''))
            #os.remove(py)
            print py
    bak.close()
