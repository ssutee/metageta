# -*- coding: latin-1 -*-
import os,sys,shutil,glob,tempfile,zipfile as zip

sys.path.append('..')
from setenv import BIN_DIR,DOWNLOAD_DIR
from utilities import rglob,which,runcmd

def main():
    if len(sys.argv)>1:
        vers=sys.argv[1]
        pause=False
    else:
        vers=''
        pause=True
        
    svn=which('svn')
    makensis=which('makensis')

    if not svn:
        print 'Install an SVN command line client (e.g. http://www.sliksvn.com) or ensure that it is on your PATH'
        if pause:raw_input('Press enter to exit.')
        sys.exit(1)

    if not makensis:
        print 'Install NSIS (http://nsis.sourceforge.net) or ensure that it is on your PATH'
        if pause:raw_input('Press enter to exit.')
        sys.exit(1)

    if not vers:
        try:vers = raw_input('Enter the version to build, options are \n1.N (eg. 1.1), curr (latest release),  trunk (unstable development):  ')
        except:sys.exit(0)#vers = 'trunk'
        if vers in ['curr','']:
            cmd='svn ls http://metageta.googlecode.com/svn/tags'
            exit_code,stdout,stderr=runcmd(cmd)
            if exit_code != 0:
                if stderr:    print stderr
                elif stdout:  print stdout
                else :        print 'SVN command failed'
                raw_input('Press enter to exit.')
                sys.exit(exit_code)
            else:
                vers=stdout.strip().split()[-1][:-1]
                print 'Latest release is %s'%vers

    cd = os.path.abspath(os.path.dirname(sys.argv[0]))
    td = os.path.dirname(cd)

    os.chdir(cd)
    tmp=tempfile.mkdtemp(dir=cd)

    ##########################################################
    ##Get revision
    if vers == 'trunk':repo='trunk'
    else:repo='tags/'+vers
        
    cmd='svn info http://metageta.googlecode.com/svn/%s'%repo
    exit_code,stdout,stderr=runcmd(cmd)
    if exit_code != 0:
        print stderr
        if pause:raw_input('Press enter to exit.')
        cleanup(tmp)
        sys.exit(exit_code)
        
    for line in stdout.split('\n'):
        line=line.split(':')
        if line[0].strip()=='Last Changed Rev':
            rev=line[1].strip()
            break

    if vers == 'trunk':
        outfile='trunk-rev'+rev
        #vers='0.0.0.'+rev
    else:
        #outfile=vers
        vers=vers+'.0.'+rev
        outfile=vers

    ##########################################################
    print 'Cleaning up compiled objects'
    for pyco in rglob(td+'\\bin','*.py[c|o]'):
        os.remove(pyco)

    ##########################################################
    print 'Exporting from SVN repo'
    cmd='svn export -q --force http://metageta.googlecode.com/svn/%s %s/metageta'%(repo,tmp)
    exit_code,stdout,stderr=runcmd(cmd)
    if exit_code != 0:
        if stderr:    print stderr
        elif stdout:  print stdout
        else :        print 'SVN export failed'
        cleanup(tmp)
        if pause:raw_input('Press enter to exit.')
        sys.exit(exit_code)

    ##########################################################
    f=open('%s/version.txt'%tmp,'w').write('Version: %s'%vers)
    for f in glob.glob('include/*'):
        if os.path.basename(f) != 'license.rtf': shutil.copy(f,tmp)

    ##########################################################
    print 'Compiling NSIS installer'
    setup=DOWNLOAD_DIR+r'\metageta-%s-setup.exe'%outfile
    if vers == 'trunk':cmd=r'makensis /V2 /DAPP_DIR=%s /DBIN_DIR=%s /DOUTPATH=%s buildmetageta.nsi'%(tmp,setenv.BIN_DIR,setup)
    else:              cmd=r'makensis /V2 /DAPP_DIR=%s /DBIN_DIR=%s /DOUTPATH=%s /DVERSION=%s buildmetageta.nsi'%(tmp,setenv.BIN_DIR,setup,vers)
    exit_code,stdout,stderr=runcmd(cmd)
    if exit_code != 0:
        if stderr and stdout:
            sys.stderr.write(stderr)
            sys.stdout.write(stdout)
        elif stderr:  sys.stderr.write(stderr)
        elif stdout:  sys.stdout.write(stdout)
        else :        sys.stderr.write('NSIS installer compile failed')
        cleanup(tmp)
        raw_input('Press enter to exit.')
        sys.exit(exit_code)

    ##########################################################
    print 'Zipping files'
    fout='../downloads/metageta-%s.zip'%outfile
    zout=zip.ZipFile(fout,'w',zip.ZIP_DEFLATED)

    #Code only    
    for f in rglob(tmp):
        if not f==sys.argv[0]:
            zout.write(f,f.replace(tmp,'metageta/'))
    zout.close()

    #No installer
    shutil.copyfile(fout,fout.replace('.zip','_pygdal.zip'))
    zout=zip.ZipFile(fout.replace('.zip','_pygdal.zip'),'a',zip.ZIP_DEFLATED)
    for f in rglob('../bin'):
        f=os.path.abspath(f)
        zout.write(f,f.replace(td,'metageta/'))
    zout.close()

    #With installer
    zout=zip.ZipFile(fout.replace('.zip','_pygdal-installer.zip'),'w',zip.ZIP_DEFLATED)
    zout.write(setup, os.path.basename(setup))
    zout.close()

    cleanup(tmp)
    if pause:raw_input('Press enter to exit.')

def cleanup(*args):
    for arg in args:
        if os.path.isdir(arg):
            try:shutil.rmtree(arg)
            except Exception,err:
                print err
        elif os.path.isfile(arg):
            try:os.remove(arg)
            except Exception,err:
                print err
        else:pass

if __name__=='__main__':
    main()