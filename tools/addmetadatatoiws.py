import sqlite3 as sqlite
from metageta import utilities

def main(iws,site,port,xls):

    db=r"\\%s\C$\Intergraph\APOLLO Essentials\config\filelist.db"%iws
    xlrdr=utilities.ExcelReader(xls, dict)
    con=sqlite.connect(db)

    html_url='http://%s:%s/geonetwork/srv/en/metadata.show?uuid=%s'
    xml_url='http://%s:%s/geonetwork/srv/en/xml.metadata.get?uuid=%s'
    custom_tag=('<MetadataURL type="ISO19115:2003">'
                '   <Format>text/xml</Format>'
                '   <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="%s" />'
                '</MetadataURL>'
                '<MetadataURL>'
                '    <Format>text/html</Format>'
                '    <OnlineResource xmlns:xlink="http://www.w3.org/1999/xlink" xlink:type="simple" xlink:href="%s" />'
                '</MetadataURL>')
    #abstract_tag='<![CDATA[%s]]>'
    for rec in xlrdr:
        deleted=rec.get('deleted',0)
        if deleted in [1,'1']:continue
        filepath=rec['filepath']
        abstract=rec.get('abstract',None)
        use_constraints=rec.get('useConstraints',None)
        try:fid=filepath.split('iwsimages')[1].replace('\\','/')
        except IndexError:continue
        fid=unicode(fid)
        capabilities_abstract=['Metadata URL: '+html_url%(site,port,rec['guid'])]
        if use_constraints:capabilities_abstract.append('Use Constraints: '+use_constraints)
        if abstract:capabilities_abstract.append('Abstract: ' + abstract)
        #capabilities_abstract= unicode(abstract_tag%'<br />'.join(capabilities_abstract).decode('utf8'))
        capabilities_abstract= unicode('<br />'.join(capabilities_abstract).decode('utf8'))
        custom_tags=custom_tag%(xml_url%(site,port,rec['guid']),html_url%(site,port,rec['guid']))
        cur=con.execute('update Dataset set CapabilitiesAbstract = ? where lower(FullName) = ?', (capabilities_abstract, fid))
        cur=con.execute('update Dataset set WMSCustomTags = ? where lower(FullName) = ?', (custom_tags, fid))
    con.commit()

if __name__ == '__main__':
    import argparse
    argparser=argparse.ArgumentParser()
    argparser.add_argument('-i','--iws', dest='iws', help='Apollo Server')
    argparser.add_argument('-s','--site', dest='site', help='Geonetwork site')
    argparser.add_argument('-p','--port', dest='port', help='Geonetwork port', default="8080")
    argparser.add_argument('-x','--xls', dest='xls', help='Crawl result file')
    args = argparser.parse_args()
    main(args.iws,args.site,args.port,args.xls)
