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
# Usage: ANZLICGeographicExtentsToGeonetworkSkosThesaurus.py [options] output_RDF
#
#   Generate Geonetwork Skos Thesaurus RDF for ANZLIC Geographic Descriptions
#
#   Options:
#     -h, --help            show this help message and exit
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

region='''<skos:Concept rdf:about="http://geonetwork-opensource.org/regions#%s">
    <skos:prefLabel xml:lang="en">%s</skos:prefLabel>
    <skos:inScheme rdf:resource="http://geonetwork-opensource.org/regions" />
    %s
  </skos:Concept>'''

subregion='''<skos:Concept rdf:about="http://geonetwork-opensource.org/regions#%s">
    <skos:prefLabel xml:lang="en">%s</skos:prefLabel>
    <gml:BoundedBy>
      <gml:Envelope gml:srsName="http://www.opengis.net/gml/srs/epsg.xml#epsg:4326">
        <gml:lowerCorner>%s %s</gml:lowerCorner>
        <gml:upperCorner>%s %s</gml:upperCorner>
      </gml:Envelope>
    </gml:BoundedBy>
    <skos:broader rdf:resource="http://geonetwork-opensource.org/regions#%s" />
  </skos:Concept>'''

narrower='<skos:narrower rdf:resource="http://geonetwork-opensource.org/regions#%s" />'

startxml='''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:fn="http://www.w3.org/2005/02/xpath-functions" xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:gml="http://www.opengis.net/gml#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:skos="http://www.w3.org/2004/02/skos/core#" xmlns:xdt="http://www.w3.org/2005/02/xpath-datatypes" xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <!-- Scheme -->
  <skos:ConceptScheme rdf:about="http://geonetwork-opensource.org/regions">
    <dc:title>Region</dc:title>
    <dc:description>ANZLIC Geographic Extents</dc:description>
    <dc:creator>
      <foaf:Organization>
        <foaf:name>DSEWPaC</foaf:name>
      </foaf:Organization>
    </dc:creator>
    <dc:rights>Free to all for non commercial use.</dc:rights>
    <dcterms:issued>2011-10-25</dcterms:issued>
    <dcterms:modified>2011-10-25</dcterms:modified>
  </skos:ConceptScheme>'''

endxml='</rdf:RDF>'

def main(url,config,output):
    doc=etree.parse(os.path.basename(url))
    root = doc.getroot() # CT_CodelistCatalogue
    namespaces={'gmx':'http://www.isotc211.org/2005/gmx',
                'gml':'http://www.opengis.net/gml'}

    outfile=open(output,'w')
    outfile.write(startxml)
    regions=[]
    cld_all=root.findall('.//gmx:codelistItem/gmx:CodeListDictionary',namespaces=namespaces)
    for cld in cld_all:
        subregions=[]
        narrowers=[]
        regionid=cld.attrib['{%s}id'%namespaces['gml']]
        regiondesc= cld.find('gml:description',namespaces=namespaces)
        regionname=regiondesc.text.split()[0]
        if regionid in config or not config:
            for cd in cld.findall('gmx:codeEntry/gmx:CodeDefinition',namespaces=namespaces):
                desc=cd.find('gml:description',namespaces=namespaces).text.split('|')
                id=cd.find('gml:identifier',namespaces=namespaces).text.strip()
                name=desc[0]
                ymax,ymin,xmax,xmin=[float(s) for s in desc[1:-1]]
                subregions.append(subregion%(id,name,xmin,ymin,xmax,ymax,regionid))
                narrowers.append(narrower%id)
            outfile.write(region%(regionid,regionname,'\n'.join(narrowers)))
            outfile.write('\n'.join(subregions))
    outfile.write(endxml)

if __name__ == '__main__':
    import csv, optparse #optparse deprecated in py2.7, will need to switch to argparse

    #Defaults
    config='%s.config'%(os.path.splitext(os.path.basename(__file__))[0])
    url='http://asdd.ga.gov.au/asdd/profileinfo/anzlic-allgens.xml'

    #Parse command line args
    description='Generate Geonetwork Skos Thesaurus RDF for ANZLIC Geographic Descriptions'
    usage = "usage: %prog [options] output_RDF"
    parser = optparse.OptionParser(description=description,usage=usage)
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
