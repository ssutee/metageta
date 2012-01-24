# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        GeographicDescription.py
# Purpose:     Generate GeographicDescription for metageta crawl results
#
# Author:      Luke Pinner, DSEWPaC
#
# Created:     16/01/2012
# Copyright:   (c) DSEWPaC 2012
# Licence:     MIT/X
#
# Logic:
#  * Check minimum bounding rectangle (MBR) of of crawl result,
#    - if it is > 270° wide and > 135° high, call it global and stop processing
#    - if it is > 180° wide and > 67.5° high and in a single hemisphere
#      call it N or S Hemisphere and stop processing
#  * Intersect MBR with Comm Marine Area FE, if contained:
#      - Intersect with Australia MBR, if intersects:
#        * if area >= 75% of Aus MBR, call it Australia and stop processing
#        * else:intersect with State/Terr and select state with most overlap
#        * if area >= 75% of selected State poly MBR, call it state/terr name and stop processing
#        * else: loop through defined local datasets and intersect, assign up to 100 that intersect
#      - else: intersect with World countries
#  * else: intersect with World countries
#
#
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python

#Imports
import os,sys
from osgeo import ogr
sys.path.insert(0,r'C:\Program Files (x86)\MetaGETA\metageta')
from metageta import utilities, geometry
config = __import__('%s_config'%(os.path.splitext(os.path.basename(__file__))[0]))
ogr.UseExceptions()

def main(inxls,outxls):
    world_layers=[]
    continental_layers=[]
    local_layers=[]
    for p,f in config.world:
        ds=ogr.Open(p)
        world_layers.append([ds,f])
    for p,f in config.continental:
        ds=ogr.Open(p)
        continental_layers.append([ds,f])
    for p,f in config.local:
        ds=ogr.Open(p)
        local_layers.append([ds,f])

    #How many results do we return per layer?
    nlocals=len(config.local)
    maxintersects=100
    nintersects=maxintersects/nlocals

    xlr=utilities.ExcelReader(xls,list)
    fields = xlr.headers

    #Don't try and update existing results, just redo them.
    while True:
        try:del fields[fields.index('GeographicDescription')]
        except:break
    for i in range(maxintersects):fields.append('GeographicDescription')

    ExcelWriter=utilities.ExcelWriter(out, fields=fields, sort=False)

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
            ExcelWriter.WriteRecord(zip(hdr,rec))
            continue

        #Get the MBR and run the intersections
        ll,ur=rec[hdr.index('LL')],rec[hdr.index('UR')]
        xmin,ymin,xmax,ymax=[float(f) for f in ll.split(',') + ur.split(',')]
        region=regions([xmin,ymin,xmax,ymax],world_layers,continental_layers,local_layers,nintersects)

        #Add to the existing record and write out
        for r in region:
            hdr.append('GeographicDescription')
            rec.append(r)

        ExcelWriter.WriteRecord(zip(hdr,rec))


def intersect(geom,lyr,field,mbronly=False, maxintersects=0):
    lyr.SetSpatialFilter(geom)
    lyr.ResetReading()
    area=geom.Area()
    intersections=[]
    try:
        for i,feat in enumerate(lyr):
            if maxintersects and i >= maxintersects:break
            fi=feat.GetFieldIndex(field)
            attribute=feat.GetFieldAsString(fi)
            if mbronly:
                intersections.append(attribute)
            else:
                featgeom=feat.GetGeometryRef()
                overlap=geom.Intersection(featgeom)
                intersections.append([overlap.Area(),featgeom.Area(),attribute])
    except Exception as err:
        print err

    lyr.SetSpatialFilter(None)
    return intersections

def nearest(geom,lyr,field, maxintersects=0):
    lyr.SetSpatialFilter(geom)
    lyr.ResetReading()
    attributes=[]
    distances=[]
    centroid=geom.Centroid()
    for i,feat in enumerate(lyr):
        fi=feat.GetFieldIndex(field)
        attribute= feat.GetFieldAsString(fi)
        distance = centroid.Distance(feat.GetGeometryRef())
        try:
            if distance < max(distances):
                distances.insert(0,distance)
                attributes.insert(0,attribute)
            elif maxintersects and i < maxintersects:
                distances.append(distance)
                attributes.append(attribute)
            else: break
        except:
            distances.insert(0,distance)
            attributes.insert(0,attribute)


    lyr.SetSpatialFilter(None)

    sdistances=sorted(zip(distances,attributes))
    if maxintersects:return sdistances[:maxintersects]
    else: return sdistances


def regions(extent, world, continental,local, maxintersects=0):

    global_ext=(270,135)
    hsphere_ext=(180,67.5)
    #MBR of Commonwealth Marine areas
    extent1=[39.5,-70,173.5, -7.5]
    #MBR of Aus coastline (inc. Norfolk)
    extent2=[112,-44,159.5, -9]

    xmin,ymin,xmax,ymax=extent
    if (xmax-xmin)>global_ext[0] and (ymax-ymin)>=global_ext[1]:
       return ['Global']

    elif xmax-xmin>hsphere_ext[0] and ymax-ymin>=hsphere_ext[1] and ymax> 0 and ymin >= 0:
            return ['Northern Hemisphere']
    elif xmax-xmin>hsphere_ext[0] and ymax-ymin>=hsphere_ext[1] and ymax < 0 and ymin < 0:
             return ['Southern Hemisphere']
    else:
        geom=geometry.GeomFromExtent(extent)
        mbr1 = geometry.GeomFromExtent(extent1)
        if mbr1.Contains(geom):
            mbr2 = geometry.GeomFromExtent(extent2)
            int2=mbr2.Intersection(geom).Area()
            if int2 > (0.75 * mbr2.Area()):
                return ['Australia']
            else:
                regionnames=[]
                for ds,field in continental:
                    lyr=ds.GetLayer()
                    intersections = intersect(geom,lyr,field)
                    if intersections:
                        names=[]
                        states=[]
                        for overlaparea, featurearea, name in intersections:
                            if overlaparea/featurearea>0.75:names.append(name)
                        if names:return names
                        else:regionnames=list(names)

                for i,ds_field in enumerate(local):
                    ds,field=ds_field
                    lyr=ds.GetLayer()
                    lyrtype=ogr.GeometryTypeToName(lyr.GetGeomType()).upper()
                    if 'POINT' in lyrtype:
                        try:distance,names=zip(*nearest(geom,lyr,field, maxintersects))
                        except ValueError:continue
                        regionnames+=list(names)
                    else:
                        regionnames+=list(intersect(geom,lyr,field, True, maxintersects))

                return regionnames

    #Doesn't meet any of the other conditions, try the world layer/s
    regionnames=[]
    for i,ds_field in enumerate(world):
        ds,field=ds_field
        lyr=ds.GetLayer()
        lyrtype=ogr.GeometryTypeToName(lyr.GetGeomType()).upper()
        if 'POINT' in lyrtype:
            try:distance,names=zip(*nearest(geom,lyr,field, maxintersects))
            except ValueError:continue
            regionnames+=list(names)
        else:
            regionnames+=list(intersect(geom,lyr,field, True, maxintersects))

    return regionnames

if __name__ == '__main__':
    if len(sys.argv) != 3:
        del sys.argv[1:]
        sys.argv.append(raw_input("Enter the input XLS: "))
        sys.argv.append(raw_input("Enter the output XLS: "))

    xls,out=sys.argv[1:3]
    try:err=os.path.samefile(f1, f2)
    except AttributeError:err=os.path.abspath(xls).lower()==os.path.abspath(out).lower()
    if err:raise(ValueError('Output spreadsheet can not be the same as the input!'))
    if not os.path.exists(xls):raise(ValueError('Input spreadsheet does not exist!'))

    main(xls,out)
