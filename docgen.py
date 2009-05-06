'''Generate PyDoc documentation'''

import os,formats,subprocess,glob,sys

def runcmd(cmd, format='s'):
    proc = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if format.lower() == 's': #string output
        stdout,stderr=proc.communicate()
    #elif format.lower() == 'f': #file object output #BUG doesn't flush IO buffer, causes python to hang
    #    stdout,stderr=proc.stdout,proc.stderr
    elif format.lower() == 'l': #list output
        stdout,stderr=proc.stdout.readlines(),proc.stderr.readlines()
    #else:raise TypeError, "fomat argument must be in ['s','f','l'] (string, file, list)"
    else:raise TypeError, "fomat argument must be in ['s','l'] (string or list format)"
    exit_code=proc.wait()
    return exit_code,stdout,stderr

pydoc='%s\\Lib\\pydoc.py' % os.environ['PYTHONHOME']
pyw='%s\\pythonw.exe' % os.environ['PYTHONHOME']

curdir=os.path.abspath(os.curdir)
os.chdir('%s\\Doc' % os.environ['CURDIR'])

for py in glob.glob('../lib/*.py'):
    exit_code,stdout,stderr=runcmd('"%s" "%s" -w %s'%(pyw,pydoc,os.path.basename(py)[:-3]))
    if exit_code == 0:print stdout
    else: print exit_code,stderr


exit_code,stdout,stderr=runcmd('"%s" "%s" -w formats'%(pyw,pydoc))
if exit_code == 0:print stdout
else: print stderr
for format in formats.__formats__:
    exit_code,stdout,stderr=runcmd('"%s" "%s" -w formats.%s'%(pyw,pydoc,format))
    if exit_code == 0:print stdout
    else: print stderr
exit_code,stdout,stderr=runcmd('"%s" "%s" -w transforms'%(pyw,pydoc))
if exit_code == 0:print stdout
else: print stderr

os.chdir(curdir)
