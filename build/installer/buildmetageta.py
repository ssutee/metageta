# -*- coding: latin-1 -*-
'''
    Build the MetaGETA download packages, including the NSIS executable

    Usage: buildmetageta.py [version]
    Where: version = tagged release number (e.g. 1.2), "curr" - latest release, "trunk" - unstable dev.

    NOTE: Versions <= 1.2 only work with OSGeo4W/Python25 binaries.
          You need to override setenv.py defaults with environment variables before running the build.
'''
import os,sys,shutil,glob,tempfile,zipfile as zip, fnmatch

sys.path.append('..')
sys.path.append(os.path.dirname(os.path.dirname(sys.argv[0])))
from setenv import BIN_DIR,DOWNLOAD_DIR,TOPDIR
from utilities import rglob,which,runcmd

#Allow overwriting of the environment variables
def main():
    try:
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
            try:vers = raw_input('Enter the version to build, options are: \n1.N (eg. 1.1 release) \ncurr (latest release) \nbranches/<branch> \ntrunk (unstable development) \nVersion:  ')
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

        os.chdir(cd)
        tmp=tempfile.mkdtemp(dir=cd)

        ##########################################################
        ##Get revision
        if vers == 'trunk':repo='trunk'
        elif 'branches/'in vers:repo=vers
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
        elif 'branches/'in vers:
            outfile='%s-rev%s'%(vers.replace('/','-'),rev)
        else:
            vers=vers+'.0.'+rev
            outfile=vers

        ##########################################################
        print 'Cleaning up compiled objects'
        for pyco in rglob(BIN_DIR,'*.py[c|o]'):
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
        f=open('%s\\version.txt'%tmp,'w').write('Version: %s'%vers)
        for f in glob.glob('include\\*'):shutil.copy(f,tmp)
            
        ##########################################################
        excluded_files=[]
        for f in open('excluded_files.txt'):
            f=f.split('#')[0].strip() #Handle comments
            if f:excluded_files.append(f)
            
        ##########################################################
        print 'Compiling NSIS installer'
        setup=DOWNLOAD_DIR+r'\metageta-%s-setup.exe'%outfile
        if vers == 'trunk' or 'branches/'in vers:
            cmd=r'makensis /V2 /DEXCLUDE=%s /DAPP_DIR=%s /DBIN_DIR=%s /DOUTPATH=%s  /DDISPLAY_VERSION=%s buildmetageta.nsi'%('"/x %s"'%' /x '.join(excluded_files),tmp,BIN_DIR,setup,outfile)
        else:
            cmd=r'makensis /V2 /DEXCLUDE=%s /DAPP_DIR=%s /DBIN_DIR=%s /DOUTPATH=%s /DVERSION=%s /DDISPLAY_VERSION=%s buildmetageta.nsi'%('"/x %s"'%' /x '.join(excluded_files),tmp,BIN_DIR,setup,vers,vers)
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

        setup=DOWNLOAD_DIR+r'\metageta-%s-plugins-setup.exe'%outfile
        if vers == 'trunk' or 'branches/'in vers:
            cmd=r'makensis /V2 /DAPP_DIR=%s /DBIN_DIR=%s /DOUTPATH=%s  /DDISPLAY_VERSION=%s buildmetageta-plugins.nsi'%(tmp,BIN_DIR,setup,outfile)
        else:
            cmd=r'makensis /V2 /DAPP_DIR=%s /DBIN_DIR=%s /DOUTPATH=%s /DVERSION=%s /DDISPLAY_VERSION=%s buildmetageta-plugins.nsi'%(tmp,BIN_DIR,setup,vers,vers)
        exit_code,stdout,stderr=runcmd(cmd)
        if exit_code != 0:
            if stderr and stdout:
                sys.stderr.write(stderr)
                sys.stdout.write(stdout)
            elif stderr:  sys.stderr.write(stderr)
            elif stdout:  sys.stdout.write(stdout)
            else :        sys.stderr.write('NSIS plugin installer compile failed')
            cleanup(tmp)
            raw_input('Press enter to exit.')
            sys.exit(exit_code)

        ##########################################################
        print 'Zipping files'
        fout=DOWNLOAD_DIR+'\\metageta-%s.zip'%outfile
        zout=zip.ZipFile(fout,'w',zip.ZIP_DEFLATED)

        #Code only    
        for f in rglob(tmp):
            if not os.path.isdir(f):
                inc=True
                for exc in excluded_files:
                    if fnmatch.filter(f.split(os.path.sep), exc):
                        inc=False
                        break
                if inc:
                    zout.write(f,f.replace(tmp,'metageta'))
        zout.close()

        #No installer
        #shutil.copyfile(fout,fout.replace('.zip','-pygdal.zip'))
        #zout=zip.ZipFile(fout.replace('.zip','-pygdal.zip'),'a',zip.ZIP_DEFLATED)
        #for f in rglob(BIN_DIR):
        #    if not os.path.isdir(f):
        #        inc=True
        #        for exc in excluded_files:
        #            if fnmatch.filter(f.split(os.path.sep), exc):
        #                inc=False
        #                break
        #        if inc:
        #            f=os.path.abspath(f)
        #            zout.write(f,f.replace(TOPDIR,'metageta'))
        #zout.close()

        #With installer
        zout=zip.ZipFile(fout.replace('.zip','-setup.zip'),'w',zip.ZIP_DEFLATED)
        zout.write(setup, os.path.basename(setup))
        zout.close()
    
    except Exception,err:
        print err

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