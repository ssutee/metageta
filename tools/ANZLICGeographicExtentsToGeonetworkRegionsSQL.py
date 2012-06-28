# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        ANZLICGeographicExtentName.py
# Purpose:     Generate GeographicDescription for metadata crawl results using
#              the extent of place names in the standard ANZLIC codelist:
#              'http://asdd.ga.gov.au/asdd/profileinfo/anzlic-allgens.xml'
#
# Author:      Luke Pinner, DSEWPaC
#
# Created:     07/02/2012
# Copyright:   (c) DSEWPaC 2012
# Licence:     MIT/X
#
# Usage: ANZLICGeographicExtentName.py [options] input_xls output_xls
#
#   Generate ANZLIC Geographic Descriptions for metadata crawl results using the
#   extent of place names in the standard ANZLIC
#   codelist:http://asdd.ga.gov.au/asdd/profileinfo/anzlic-allgens.xml
#
#   Options:
#     -h, --help            show this help message and exit
#     -a, --all             Intersect against all ANZLIC geographic description
#                           extents, including UnZud.
#     -c config, --config=config
#                           description code list items. Default:
#                           ANZLICGeographicExtentName.config
#     -u url, --url=url     URL of ANZLIC geographic description codelist.
#                           Default: http://asdd.ga.gov.au/asdd/profileinfo
#                           /anzlic-allgens.xml
#-------------------------------------------------------------------------------

import os,sys
try:from lxml import etree
except ImportError:raise ImportError('lxml is not installed. It is available from http://pypi.python.org/pypi/lxml')

Regions='INSERT INTO Regions VALUES (%s,%s,%s,%s,%s);' #id,ymax,ymin,xmin,xmax
RegionsDes="INSERT INTO RegionsDes VALUES  (%s,'en','%s:%s');"

def main(url,config,output):
    doc=etree.parse(os.path.basename(url))
    root = doc.getroot() # CT_CodelistCatalogue
    namespaces={'gmx':'http://www.isotc211.org/2005/gmx',
                'gml':'http://www.opengis.net/gml'}

    outfile=open(output,'w')
    outfile.write('DELETE FROM RegionsDes;\nDELETE FROM Regions;\n')

    cld_all=root.findall('.//gmx:codelistItem/gmx:CodeListDictionary',namespaces=namespaces)
    id=0
    for cld in cld_all:
        regionid=cld.attrib['{%s}id'%namespaces['gml']]
        regiondesc= cld.find('gml:description',namespaces=namespaces)
        regionname=' '.join(regiondesc.text.split()[0:-1]).replace("'","''")
        if regionid in config or not config:
            for cd in cld.findall('gmx:codeEntry/gmx:CodeDefinition',namespaces=namespaces):
                desc=cd.find('gml:description',namespaces=namespaces).text.split('|')
                name=desc[0].replace("'","''")
                ymax,ymin,xmax,xmin=[float(s) for s in desc[1:-1]]
                outfile.write(Regions%(id,ymax,ymin,xmin,xmax)+'\n')
                outfile.write(RegionsDes%(id,regionname,name)+'\n')
                id+=1

if __name__ == '__main__':
    import csv, optparse #optparse deprecated in py2.7, will need to switch to argparse

    #Defaults
    config='%s.config'%(os.path.splitext(os.path.basename(__file__))[0])
    url='http://asdd.ga.gov.au/asdd/profileinfo/anzlic-allgens.xml'

    #Parse command line args
    description='Generate ANZLIC Geographic Descriptions for metadata crawl results using the extent of place names in the standard ANZLIC codelist:%s'%url
    usage = "usage: %prog [options] input_xls output_xls"
    parser = optparse.OptionParser(description=description,usage=usage)
    opt=parser.add_option("-a", "--all", dest="all", metavar="all",
        action="store_true",default=False,
        help="Intersect against all ANZLIC geographic description extents, including UnZud.")
    opt=parser.add_option("-c", "--config", dest="config", metavar="config",
        default=config,
        help="Config file containing list of ANZLIC geographic description code list items. Default: %s"%config)
    opt=parser.add_option("-u", "--url", dest="url", metavar="url",
        default=url,
        help="URL of ANZLIC geographic description codelist. Default: %s"%url)

    optvals,argvals = parser.parse_args()

    #Check required positional args
    if not argvals:
        argvals=[]
        try:
            arg=raw_input("Enter the output RDF: ")
            if arg:argvals.append(arg)
        except:pass

    if not argvals:
        parser.print_help()
        sys.exit(1)

    config=open(optvals.config,'rb').read().split()
    main(optvals.url,config,argvals[0])
