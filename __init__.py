'''Utility functions to assist XSL transforms'''
from glob import glob as _glob
import os.path as _path
import StringIO as _strio
from Ft.Xml.Xslt import Transform as _Transform
from Ft.Xml import Parse as _Parse
from Ft.Xml import Domlette as _Dom

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
        xslfile = _path.join(__path__[0],_xslfiles[transform])
    elif _path.exists(transform):    #Have we been passed an XSL file path...?
        xslfile=transform
    else: raise ValueError, 'Can not transform using %s!' % transform
    result = _Transform(inxmlstring, xslfile, output=open(outxmlfile, 'w'))

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
    xmldir=os.path.dirname(xmlfile)
    curdir=os.path.abspath(os.curdir)
    os.chdir(outdir)
    try:
        mef=zipfile.ZipFile(r'%s.mef'%(uid),'w',zipfile.ZIP_DEFLATED)
        os.mkdir(uid)
        os.chdir(uid)
        shutil.copy(xmlfile,'metadata.xml')
        if overviews:
            os.mkdir('public')
            for f in overviews:
                shutil.copy(f,os.path.join('public',os.path.basename(f)))
        _CreateInfo(uid,overviews)
        shutil.copy(xmlfile,'metadata.xml')
        for f in rglob('.'):
            if not os.path.isdir(f): mef.write(f)
        mef.close()
        del mef
    finally:
        os.chdir(outdir)
        shutil.rmtree(uid)
        os.chdir(curdir)
        
#++++++++++++++++++++++++
#Private methods    
#++++++++++++++++++++++++
def _CreateInfo(uid,overviews=[]):
    now = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime())
    if overviews:format='partial'
    else:format='simple'

    general={'createDate':now,'changeDate':now,'schema':'iso19139','isTemplate':'false','format':format,'uuid':uid}
    privileges = ['view','editing','dynamic','featured']

    doc=Dom.implementation.createRootNode('file:///info.xml')
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
            child.setAttributeNS(None, 'name',os.path.basename(f))
            parent.appendChild(child)
        root.appendChild(parent)

    doc.appendChild(root)
    Dom.PrettyPrint(doc,open('info.xml','w'))
