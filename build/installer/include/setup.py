#!/usr/bin/python
from distutils.core import setup
import os,sys,warnings,shutil

def getpaths():
    #fake a setup to get the paths
    lib,scripts,data,prefix=('','','','')
    args=sys.argv[:]
    idx=sys.argv.index('install')
    sys.argv.insert(idx,'-q')
    sys.argv.insert(idx,'--dry-run')
    s=setup()
    lib=s.command_obj['install'].install_lib
    scripts=s.command_obj['install'].install_scripts
    data=s.command_obj['install'].install_data
    prefix=s.command_obj['install'].prefix
    sys.argv=args[:]
    return lib,scripts,data,prefix

if __name__=='__main__':
    version=open('version.txt').read().split()[1]
    os.chdir('metageta')

    setupargs={'name':'MetaGETA',
          'version':version,
          'description':'Metadata Gathering, Extraction and Transformation Application',
          'long_description':'MetaGETA is a python application for discovering and extracting metadata from spatial raster datasets (metadata crawler) and transforming it into xml (metadata transformation). A number of generic and specialised imagery formats are supported. The format support has a plugin architecture and more formats can easily be added.',
          'platforms':['linux','windows','darwin'],
          'author':'Luke Pinner and Simon Oliver',
          'author_email':'pinner [dot] luke [at] removethistext gmail [dot] com',
          'url':'http://code.google.com/p/metageta',
          'license':'MIT License',
          'classifiers':['Development Status :: 4 - Beta',
                       'Environment :: Win32 (MS Windows)',
                       'Environment :: X11 Applications',
                       'Intended Audience :: End Users/Desktop',
                       'Intended Audience :: Developers',
                       'License :: OSI Approved :: MIT License',
                       'Operating System :: POSIX :: Linux',
                       'Operating System :: Microsoft :: Windows',
                       'Programming Language :: Python',
                       'Topic :: Scientific/Engineering :: GIS'],
          'packages':['metageta','metageta.formats','metageta.transforms'],
          'requires':['osgeo.gdal','lxml','xlutils','xlwt','xlrd'],          
          'scripts':['runcrawler.py','runtransform.py'],
          'package_data':{'metageta': ['config/config.xml']}
        }

    if 'install' in sys.argv:
        lib,scripts,data,prefix=getpaths()
        errors=[]
        try:
            from osgeo import gdal
            v=gdal.VersionInfo("RELEASE_NAME")
            assert [int(i) for i in gdal.VersionInfo("RELEASE_NAME").split('.')] >= [1,6,0]
            print 'Found GDAL %s Ok.'%v
        except ImportError:
            error='The GDAL (www.gdal.org) python bindings are not installed or not configured correctly.'
            errors.append(error)
        except AssertionError:
            error='GDAL (www.gdal.org) version %s is not supported, try upgrading.'%v
            errors.append(error)
        try:
            try:
                import xlrd, xlwt
            except:
                from xlutils import xlrd
                from xlutils import xlwt
            from xlutils import copy as xlcp
            print 'Found xlutils, xlrd and xlwt Ok.'
        except:
            error='xlutils, xlrd or xlwt is not installed or not configured correctly.'
            errors.append(error)
        try:
            import lxml
            print 'Found lxml Ok.'
        except:
            error='lxml is not installed or not configured correctly.'
            errors.append(error)
        try:
            import Tix,tkFileDialog,tkMessageBox
        except ImportError:
            import warnings
            warnings.warn('Tix, tkFileDialog and/or tkMessageBox are not installed or not configured correctly, you will not be able to use the MetaGETA GUI.')

        if errors:
            print 'MetaGETA setup can not continue. Correct the following errors and then try again:'
            print '\t'+'\n\t'.join(errors)
            sys.exit(1)

        if 'linux' in sys.platform or 'darwin' in sys.platform:
            setupargs['data_files']=[('bin',['runcrawler.py','runtransform.py'])]

    s=setup(**setupargs)

    if 'install' in sys.argv and ('linux' in sys.platform or 'darwin' in sys.platform):
        import stat
        print 'Changing mode of %s/bin/runcrawler.py|runtransform.py to 755'%data
        os.chmod(os.path.join(data,'bin/runcrawler.py'),stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
        os.chmod(os.path.join(data,'bin/runtransform.py'),stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
