'''Utility functions to assist XSL transforms'''
from glob import glob as _glob
import os.path as _path
import StringIO as _strio
import time as _time,os as _os,zipfile as _zip,shutil as _sh,sys as _sys
if __name__ == '__main__':_sys.exit(0)

from Ft.Xml.Xslt import Transform as _Transform
from Ft.Xml import Parse as _Parse
from Ft.Xml import Domlette as _Dom

from utilities import rglob as _rglob

#++++++++++++++++++++++++
#Public properties
#++++++++++++++++++++++++
transforms={}

#++++++++++++++++++++++++
#Private properties
#++++++++++++++++++++++++
_xslfiles={}

#++++++++++++++++++++++++
#Initialise pub/priv properties - load known XSL transforms
#++++++++++++++++++++++++
for _f in _glob(_path.join(__path__[0],'*.xml')):
    _xml=_Parse('file:%s'%_f)
    _name = str(_xml.xpath('string(/stylesheet/@name)'))
    _file = str(_xml.xpath('string(/stylesheet/@file)'))
    _desc = str(_xml.xpath('string(/stylesheet/@description)'))
    _xslfiles[_name]=_file
    transforms[_name]=_desc
    del _xml

#++++++++++++++++++++++++
#Public methods    
#++++++++++++++++++++++++
def Transform(inxmlstring,transform,outxmlfile):
    if _xslfiles.has_key(transform): #Is it a known XSL transform...?
        xslfile = _path.join(__path__[0],_xslfiles[transform]).replace('\\','/')
    elif _path.exists(transform):    #Have we been passed an XSL file path...?
        xslfile=_path.abspath(transform).replace('\\','/')
    else: raise ValueError, 'Can not transform using %s!' % transform
    result = _Transform(inxmlstring, 'file:///'+xslfile, output=open(outxmlfile, 'w'))

def DictToXML(dic,root):
    doc=_Dom.implementation.createRootNode('file:///%s.xml'%root)
    docelement = doc.createElementNS(None, root)
    for col in dic:
        child=doc.createElementNS(None, col)
        text=doc.createTextNode(str(dic[col]))
        child.appendChild(text)
        docelement.appendChild(child)

    doc.appendChild(docelement)
    buf=_strio.StringIO()
    _Dom.PrettyPrint(doc,stream=buf)
    return buf.getvalue()

def CreateMEF(outdir,xmlfile,uid,overviews=[]):
    '''Generate Geonetwork "Metadata Exchange Format"'''
    #Format specs @ http://www.fao.org/geonetwork/docs/ch17s02.html or http://trac.osgeo.org/geonetwork/wiki/MEF
    xmldir=_path.dirname(xmlfile)
    curdir=_path.abspath(_os.curdir)
    _os.chdir(outdir)
    try:
        mef=_zip.ZipFile(r'%s.mef'%(uid),'w',_zip.ZIP_DEFLATED)
        _os.mkdir(uid)
        _os.chdir(uid)
        _sh.copy(xmlfile,'metadata.xml')
        if overviews:
            _os.mkdir('public')
            for f in overviews:
                _sh.copy(f,_path.join('public',_path.basename(f)))
        _CreateInfo(uid,overviews)
        _sh.copy(xmlfile,'metadata.xml')
        for f in _rglob('.'):
            if not _path.isdir(f): mef.write(f)
        mef.close()
        del mef
    finally:
        _os.chdir(outdir)
        _sh.rmtree(uid)
        _os.chdir(curdir)
        
#++++++++++++++++++++++++
#Private methods    
#++++++++++++++++++++++++
def _CreateInfo(uid,overviews=[]):
    now = _time.strftime('%Y-%m-%dT%H:%M:%S',_time.localtime())
    if overviews:format='partial'
    else:format='simple'

    general={'createDate':now,'changeDate':now,'schema':'iso19139','isTemplate':'false','format':format,'uuid':uid}
    privileges = ['view','editing','dynamic','featured']

    doc=_Dom.implementation.createRootNode('file:///info.xml')
    root = doc.createElementNS(None, 'info')
    root.setAttributeNS(None, 'version','1.1')

    #General
    parent=doc.createElementNS(None, 'general')
    for key in general:
        child=doc.createElementNS(None, key)
        text=doc.createTextNode(general[key])
        child.appendChild(text)
        parent.appendChild(child)
    root.appendChild(parent)

    #Categories
    parent=doc.createElementNS(None, 'categories')
    child=doc.createElementNS(None, 'category')
    child.setAttributeNS(None, 'name','datasets')
    parent.appendChild(child)
    root.appendChild(parent)

    parent=doc.createElementNS(None, 'privileges')
    child=doc.createElementNS(None, 'group')
    child.setAttributeNS(None, 'name','all')
    for op in privileges:
        sub=doc.createElementNS(None, 'operation')
        sub.setAttributeNS(None, 'name',op)
        child.appendChild(sub)
    parent.appendChild(child)
    root.appendChild(parent)

    #Public
    if overviews:
        parent=doc.createElementNS(None, 'public')
        for f in overviews:
            child=doc.createElementNS(None, 'file')
            child.setAttributeNS(None, 'name',_path.basename(f))
            parent.appendChild(child)
        root.appendChild(parent)

    doc.appendChild(root)
    Dom.PrettyPrint(doc,open('info.xml','w'))
