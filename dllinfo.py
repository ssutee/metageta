import sys, os, utilities

for dll in utilities.rglob(os.environ['GDAL_ROOT'],'*.dll'):
    sysdll='C:/windows/system32/'+os.path.basename(dll)
    if os.path.exists(sysdll):
        #print sysdll
        cmd='%s/bin/dllupdate -oite %s'%(os.environ['GDAL_ROOT'],dll)#
        stdin,stdout,stderr=os.popen3(cmd)
        print stdout.read()
        print stderr.read()
        #print cmd