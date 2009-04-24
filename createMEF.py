from Ft.Xml import Domlette as Dom
import time,os,base64,zipfile,shutil
from lib.utilities import rglob
from lib.utilities import ExcelReader
def CreateMEF(outdir,xmlfile,uid,overviews=[]):
    fid=os.path.basename(xmlfile)[:-4]
    xmldir=os.path.dirname(xmlfile)
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
        CreateInfo(uid,overviews)
        shutil.copy(xmlfile,'metadata.xml')
        for f in rglob('.'):
            if not os.path.isdir(f): mef.write(f)
        mef.close()
        del mef
    finally:
        os.chdir(outdir)
        shutil.rmtree(uid)
        
def CreateInfo(uid,overviews=[]):
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
    
##def CreateQlk(metadata):
##    qlk=r'C:\WorkSpace\exporttest\metadata.qlk.jpg'
##    thm=r'C:\WorkSpace\exporttest\metadata.thm.jpg'
##    qlkimg=base64.encodestring(open(qlk,'rb').read())
##    thmimg=base64.encodestring(open(thm,'rb').read())
##    open(qlk+'.txt','w').write(qlkimg)
##    open(thm+'.txt','w').write(thmimg)
##    guid=metadata['guid']
##    qlk=base64.decodestring(qlkimg)
##    thm=base64.decodestring(thmimg)
##    f=open(r'public\%s.qlk.jpg'%guid, 'wb')
##    f.write(qlk)
##    f.close()
##    f=open(r'public\%s.thm.jpg'%guid, 'wb')
##    f.write(thm)
##    f.close()
