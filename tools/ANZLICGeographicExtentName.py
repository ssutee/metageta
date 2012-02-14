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
#     -m maxintersects, --maxintersects=maxintersects
#                           The number of ANZLIC geographic description codes to
#                           return per layer. Default: 5
#     -o minoverlap, --minoverlap=minoverlap
#                           The minimum proportion of the ANZLIC geographic region
#                           that the MBR of the crawl result must overlap
#                           (intersection area)/(region area). Default: 0.01
#     -f, --force           Force the command line/default maxintersects and
#                           minoverlap values to apply to all region, not just
#                           those that do not have them specified in the config
#                           Default:False
# Logic:
#  * Loop through each record in the spreadsheet generated from a metadata crawl
#  * Check minimum bounding rectangle (MBR) of the crawl result,
#    - if it is > 270° wide and > 135° high, call it global and stop processing
#    - if it is > 180° wide and > 67.5° high and in a single hemisphere
#      call it N or S Hemisphere and stop processing
#  * Intersect MBR with polygons generated from each codelistItem in the ANZLIC
#    codelist.
#    - Return at most maxintersects that meet the minoverlap criteria from a
#      list of intersections, sorted by intersection area (desc)
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os,sys
try:from lxml import etree
except ImportError:raise ImportError('lxml is not installed. It is available from http://pypi.python.org/pypi/lxml')
try:from osgeo import ogr,osr
except ImportError:raise ImportError('OGR is not installed. It is available from a number of locations:\n\thttp://gdal.org (GDAL/OGR Homepage)\n\thttp://www.gisinternals.com/sdk (Windows binaries)\n\tor your linux distros repos')
from metageta import utilities, geometry

def main(url,config,maxintersects,minoverlap,force,inxls,outxls):

    maxintersects=int(maxintersects)
    minoverlap=float(minoverlap)

    #Get a local copy of the code list
    local=os.path.basename(url)
    if not os.path.exists(local):
        # I can't be bothered trying to build an Active Directory
        # authenticated proxy handler for urllib2...
        import ctypes
        ctypes.windll.urlmon.URLDownloadToFileA(0,url,local,0,0)

    #Get code item names from the config (if any)
    configcsv=csv.DictReader(config)
    config={}
    if force:
        for rec in configcsv:
            config[rec['layer']]={'maxintersects':maxintersects,'minoverlap':minoverlap}
    else:
        for rec in configcsv:
            try:rec['maxintersects'] =int(rec['maxintersects'])
            except:rec['maxintersects']=maxintersects
            try:rec['minoverlap'] =float(rec['minoverlap'])
            except:rec['minoverlap']=minoverlap
            config[rec.pop('layer')]=rec

    #Create a polygon datasource from the code list
    ds=createANZLICDataSource(local,config)

    #How many results do we return per layer?
    nlayers=len([c for c in config if not config[c]['maxintersects']]) #ds.GetLayerCount()
    nintersects=maxintersects*nlayers+sum([config[c]['maxintersects'] for c in config if config[c]['maxintersects'] is not None])

    #Open the input spreadsheet for reading
    xlr=utilities.ExcelReader(inxls,list)
    fields = xlr.headers

    #Don't try and update existing results, just redo them.
    while True:
        try:del fields[fields.index('GeographicDescription')]
        except:break
    for i in range(nintersects):fields.append('GeographicDescription')

    #Open the output spreadsheet for writing
    xlw=utilities.ExcelWriter(outxls, fields=fields, sort=False)

    #Loop through each record and intersect with the defined layers
    for row,hdr_rec in enumerate(xlr):
        hdr,rec=map(list,zip(*hdr_rec)) #Unzip tuples and convert to lists

        while True:#Don't try and update existing results, just redo them.
            try:
                i=hdr.index('GeographicDescription')
                del hdr[i],rec[i]
            except:
                break

        try:deleted=rec[hdr.index('DELETED')]
        except:deleted=0
        if deleted==1:#Don't do intersections for layers marked deleted.
            xlw.WriteRecord(zip(hdr,rec))
            continue

        #Get the MBR and run the intersections
        ll,ur=rec[hdr.index('LL')],rec[hdr.index('UR')]
        xmin,ymin,xmax,ymax=[float(f) for f in ll.split(',') + ur.split(',')]
        region=regions([xmin,ymin,xmax,ymax],ds,'NAME',config)

        #Add to the existing record and write out
        for r in region:
            hdr.append('GeographicDescription')
            rec.append(r)

        xlw.WriteRecord(zip(hdr,rec))

def intersect(geom,lyr,field):
    lyr.SetSpatialFilter(geom)
    lyr.ResetReading()
    intersections=[]
    for i,feat in enumerate(lyr):
        fi=feat.GetFieldIndex(field)
        attribute=feat.GetFieldAsString(fi)
        featgeom=feat.GetGeometryRef()
        overlap=geom.Intersection(featgeom)
        intersections.append([overlap.Area(),featgeom.Area(),attribute])
    lyr.SetSpatialFilter(None)
    return sorted(intersections,key=lambda i:i[0]/i[1],reverse=True)

def regions(extent, ds, field,config):

    global_ext=(270,135)
    hsphere_ext=(180,67.5)

    xmin,ymin,xmax,ymax=extent
    if (xmax-xmin)>global_ext[0] and (ymax-ymin)>=global_ext[1]:
       return ['Global']
    elif xmax-xmin>hsphere_ext[0] and ymax-ymin>=hsphere_ext[1] and ymax> 0 and ymin >= 0:
            return ['Northern Hemisphere']
    elif xmax-xmin>hsphere_ext[0] and ymax-ymin>=hsphere_ext[1] and ymax < 0 and ymin < 0:
             return ['Southern Hemisphere']
    else:
        geom=geometry.GeomFromExtent(extent)
        regionnames=[]
        for i in range(0,ds.GetLayerCount()):
            lyr=ds.GetLayer(i)
            lyrname=lyr.GetName()
            maxintersects=config[lyrname]['maxintersects']
            minoverlap=config[lyrname]['minoverlap']
            intersections = intersect(geom,lyr,field)
            if intersections:
                regions_lyr=[]
                for overlaparea, featurearea, name in intersections:
                    overlap=overlaparea/featurearea
                    if overlap>minoverlap:
                        regions_lyr+=[name]
                    else:break
                regionnames+=regions_lyr[:maxintersects]
        return regionnames

def createANZLICDataSource(uri,config=[]):

    doc=etree.parse(os.path.basename(uri))
    root = doc.getroot() # CT_CodelistCatalogue
    namespaces={'gmx':'http://www.isotc211.org/2005/gmx',
                'gml':'http://www.opengis.net/gml'}
    cli_all=root.findall('.//gmx:codelistItem',namespaces=namespaces)

    # Create a memory OGR datasource to put extents in.
    mem_drv = ogr.GetDriverByName( 'Memory' )
    mem_ds = mem_drv.CreateDataSource( 'anzlic-allgens' )

    for cli in cli_all:
        cld = cli.find('gmx:CodeListDictionary',namespaces=namespaces)
        lyrid=cld.attrib['{%s}id'%namespaces['gml']]
        if lyrid in config or not config:
            mem_layer = mem_ds.CreateLayer( lyrid, None, ogr.wkbPolygon )
            fd = ogr.FieldDefn( 'ID', ogr.OFTString)
            fd.SetWidth( 25 )
            mem_layer.CreateField( fd )
            fd = ogr.FieldDefn( 'NAME', ogr.OFTString)
            fd.SetWidth( 100 )
            mem_layer.CreateField( fd )

            for cd in cld.findall('gmx:codeEntry/gmx:CodeDefinition',namespaces=namespaces):
                desc=cd.find('gml:description',namespaces=namespaces).text.split('|')
                id=cd.find('gml:identifier',namespaces=namespaces).text.strip()
                name=desc[0]
                ymax,ymin,xmax,xmin=[float(s) for s in desc[1:-1]]
                #print name,ymax,ymin,xmax,xmin
                geom=geometry.GeomFromExtent([xmin,ymin,xmax,ymax])
                feat = ogr.Feature( mem_layer.GetLayerDefn())
                feat.SetField( "ID", id )
                feat.SetField( "NAME", name )
                feat.SetGeometry(geom)
                mem_layer.CreateFeature(feat)
                feat.Destroy()

    return mem_ds

if __name__ == '__main__':
    import csv, optparse #optparse deprecated in py2.7, will need to switch to argparse

    #Defaults
    config='%s.config'%(os.path.splitext(os.path.basename(__file__))[0])
    url='http://asdd.ga.gov.au/asdd/profileinfo/anzlic-allgens.xml'
    maxintersects=5 #Max number of results to return in total
    minoverlap=0.01 #1%
    force=False

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
    opt=parser.add_option("-m", "--maxintersects", dest="maxintersects", metavar="maxintersects",
        default=maxintersects,
        help="The number of ANZLIC geographic description codes to return per layer. Default: %s"%maxintersects)
    opt=parser.add_option("-o", "--minoverlap", dest="minoverlap", metavar="minoverlap",
        default=minoverlap,
        help="The minimum proportion of the ANZLIC geographic region the the MBR of the crawl result must overlap (intersection area)/(region area). Default: %s"%minoverlap)
    opt=parser.add_option("-f", "--force", dest="force", metavar="force",
        action="store_true", default=False,
        help="Force the command line/default maxintersects and minoverlap values to apply to all regions, not just those that do not have them specified in the config. Default:%s"%force)

    optvals,argvals = parser.parse_args()

    #Check required positional args
    if len(argvals)!=2:
        argvals=[]
        try:
            arg=raw_input("Enter the input XLS: ")
            if arg:argvals.append(arg)
            arg=raw_input("Enter the output XLS: ")
            if arg:argvals.append(arg)
        except:pass

    if len(argvals)!=2 or not os.path.exists(argvals[0]):
        parser.print_help()
        sys.exit(1)

    config=open(optvals.config,'rb')
    main(optvals.url,config,optvals.maxintersects,optvals.minoverlap,optvals.force,*argvals)
    config.close()
