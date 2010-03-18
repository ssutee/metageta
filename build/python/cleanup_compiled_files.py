import sys, os.path, re
sys.path.append('..')
import setenv,utilities

i=-1
for i,pyco in enumerate(utilities.rglob(setenv.PY_DIR,'*.py[o|c]')):
    os.remove(pyco)

if i<0: print 'No files found.'
else: print 'Deleted %s files.'%(i+1)
raw_input('Press Enter to exit...')
