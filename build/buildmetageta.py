# -*- coding: latin-1 -*-
import os,sys,shutil,glob,tempfile,zipfile as zip

BIN_DIR=r'..\bin' #Path to directory containing gdal and python, relative to script.

def main():
    global BIN_DIR
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
    setup=r'..\downloads\metageta-%s-setup.exe'%outfile
    if vers == 'trunk':cmd=r'makensis /V2 /DAPP_DIR=%s /DBIN_DIR=%s /DOUTPATH=%s buildmetageta.nsi'%(tmp,BIN_DIR,setup)
    else:              cmd=r'makensis /V2 /DAPP_DIR=%s /DBIN_DIR=%s /DOUTPATH=%s /DVERSION=%s buildmetageta.nsi'%(tmp,BIN_DIR,setup,vers)
    exit_code,stdout,stderr=runcmd(cmd)
    if exit_code != 0:
        if stderr and stdout:
            sys.stderr.write(stderr)
            sys.stdout.write(stdout)
        elif stderr:  sys.stderr.write(stderr)
        elif stdout:  sys.stdout.write(stdout)
        else :        sys.stderr.write('NSIS installer compile failed')
        #cleanup(tmp)
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

def runcmd(cmd, format='s'):
    ''' Run a command
        @type     cmd:  C{str}
        @param    cmd:  Command (inc arguments) to run
        @rtype:   C{tuple}
        @return:  Returns (exit_code,stdout,stderr)
    '''
    import subprocess
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if format.lower() == 's': #string output
        stdout,stderr=proc.communicate()
    #elif format.lower() == 'f': #file object output #doesn't flush IO buffer, causes python to hang
    #    stdout,stderr=proc.stdout,proc.stderr
    elif format.lower() == 'l': #list output
        stdout,stderr=proc.stdout.readlines(),proc.stderr.readlines()
    #else:raise TypeError, "fomat argument must be in ['s','f','l'] (string, file, list)"
    else:raise TypeError, "fomat argument must be in ['s','l'] (string or list format)"
    exit_code=proc.wait()
    return exit_code,stdout,stderr

def which(name, returnfirst=True, flags=os.F_OK | os.X_OK, path=None):
    ''' Search PATH for executable files with the given name.
    
        On newer versions of MS-Windows, the PATHEXT environment variable will be
        set to the list of file extensions for files considered executable. This
        will normally include things like ".EXE". This fuction will also find files
        with the given name ending with any of these extensions.

        On MS-Windows the only flag that has any meaning is os.F_OK. Any other
        flags will be ignored.
        
        Derived mostly from U{http://code.google.com/p/waf/issues/detail?id=531} with
        additions from Brian Curtins patch - U{http://bugs.python.org/issue444582}

        @type name: C{str}
        @param name: The name for which to search.
        @type returnfirst: C{boolean}
        @param returnfirst: Return the first executable found.
        @type flags: C{int}
        @param flags: Arguments to U{os.access<http://docs.python.org/library/os.html#os.access>}.

        @rtype: C{str}/C{list}
        @return: Full path to the first matching file found or a list of the full paths to all files found, 
                 in the order in which they were found.
    '''
    result = []
    exts = filter(None, os.environ.get('PATHEXT', '').split(os.pathsep))
    if not path:
        path = os.environ.get("PATH", os.defpath)
    for p in os.environ.get('PATH', '').split(os.pathsep):
        p = os.path.join(p, name)
        if os.access(p, flags):
            if returnfirst:return p
            else:result.append(p)
        for e in exts:
            pext = p + e
            if os.access(pext, flags):
                if returnfirst:return pext
                else:result.append(pext)
    return result

class rglob:
    '''A recursive/regex enhanced glob
       adapted from os-path-walk-example-3.py - http://effbot.org/librarybook/os-path.htm 
    '''
    def __init__(self, directory, pattern="*", regex=False, regex_flags=0, recurse=True):
        ''' @type    directory: C{str}
            @param   directory: Path to xls file
            @type    pattern: C{type}
            @param   pattern: Regular expression/wildcard pattern to match files against
            @type    regex: C{boolean}
            @param   regex: Use regular expression matching (if False, use fnmatch)
                            See U{http://docs.python.org/library/re.html}
            @type    regex_flags: C{int}
            @param   regex_flags: Flags to pass to the regular expression compiler.
                                  See U{http://docs.python.org/library/re.html}
            @type    recurse: C{boolean} 
            @param   recurse: Recurse into the directory?
        '''
        self.stack = [directory]
        self.pattern = pattern
        self.regex = regex
        self.recurse = recurse
        self.regex_flags = regex_flags
        self.files = []
        self.index = 0

    def __getitem__(self, index):
        while 1:
            try:
                file = self.files[self.index]
                self.index = self.index + 1
            except IndexError:
                # pop next directory from stack
                
                self.directory = self.stack.pop()
                try:
                    self.files = os.listdir(self.directory)
                    self.index = 0
                except:pass
            else:
                # got a filename
                fullname = os.path.join(self.directory, file)
                if os.path.isdir(fullname) and not os.path.islink(fullname) and self.recurse:
                    self.stack.append(fullname)
                if self.regex:
                    import re
                    if re.search(self.pattern,file,self.regex_flags):
                        return fullname
                else:
                    import fnmatch
                    if fnmatch.fnmatch(file, self.pattern):
                        return fullname

if __name__=='__main__':
    main()