#Regular expression list of file formats
format_regex=[r'\.[lm][1-4]r$']#EO1 ALI & Hyperion

#import base dataset module
import __dataset__

# import other modules (use "_"  prefix to import privately)
import sys, os, re, glob, time, math, string
from lib import utilities
from lib import geometry

try:
    from osgeo import gdal
    from osgeo import gdalconst
    from osgeo import osr
    from osgeo import ogr
except ImportError:
    import gdal
    import gdalconst
    import osr
    import ogr
    
class Dataset(__dataset__.Dataset): #Subclass of base Dataset class
    def __init__(self,f):
        """Read Metadata for recognised EO1 ALI & Hyperion images as GDAL doesn't"""
        #http:#www.gdal.org/frmt_hdf4.html
        #Hyperion/ALI format
        #http://eo1.usgs.gov/faq.php

        gdalDataset = geometry.OpenDataset(f)
        driver=gdalDataset.GetDriver().ShortName

        f=gdalDataset.GetDescription()
        filelist=glob.glob(os.path.splitext(f)[0]+'.*')
        hdf_sd=gdalDataset.GetSubDatasets()
        hdf_md=gdalDataset.GetMetadata()

        if re.search(r'\.m[1-4]r$', f):self.metadata['sensor']='ALI'
        else:self.metadata['sensor']='HYPERION'
        
        filelist.extend(glob.glob('%s\\%s_%s_*.hdf' % (os.path.dirname(f),os.path.basename(f)[10:14],os.path.basename(f)[14:17])))

        f=f[0:-2]+'1r'
        self.metadata['filename']=os.path.split(f)[1]
        self.metadata['filepath']=f

        sd,sz = hdf_sd[0]
        sd=geometry.OpenDataset(sd)
        nbands=sd.RasterCount
        ncols=sd.RasterXSize
        if self.metadata['sensor']=='HYPERION':
            nrows=sd.RasterYSize
        else:
            sd_md=sd.GetMetadata()
            nrows=int(sd_md['Number of along track pixels']) #sd.RasterXSize is incorrect
            ncols=ncols*4-30 #Account for the four SCA strips and the overlap between SCA strips
            if len(hdf_sd) == 6:#Includes pan band (3 sds each 
                sd,sz = hdf_sd[3]
                sd=geometry.OpenDataset(sd)
                sd_md=sd.GetMetadata()
                nbands='%s,%s' % (nbands, sd_md['Number of bands'])
                ncols='%s,%s' % (ncols, int(sd_md['Number of cross track pixels'])*4-30) #Account for the four SCA strips and the overlap between SCA strips
                nrows='%s,%s' % (nrows, sd_md['Number of along track pixels'])

        self.metadata['cols'] = ncols
        self.metadata['rows'] = nrows
        self.metadata['nbands'] = nbands
        rb=sd.GetRasterBand(1)
        
        #self.metadata['datatype']=gdal.GetDataTypeName(rb.DataType)
        #self.metadata['nbits']=gdal.GetDataTypeSize(rb.DataType)
        #nodata=rb.GetNoDataValue()
        #if nodata:self.metadata['nodata']=nodata
        #else:
        #    if self.metadata['datatype'][0:4] in ['Byte','UInt']: self.metadata['nodata']=0 #Unsigned, assume 0
        #    else:self.metadata['nodata']=-2**(self.metadata['nbits']-1)                     #Signed, assume min value in data range
        #GDAL reports Int15 instead of UInt16
        self.metadata['nbits'] = 16
        self.metadata['datatype']='UInt16'
        self.metadata['nodata']=0

        cellxy=[]
        met=os.path.splitext(f)[0]+'.met'
        for line in open(met, 'r').readlines():
            if line[0:14]=='ALI Start Time':
                line=line.strip().split()
                hdf_md['ImageStartTime']=line[3]+line[4]
            if line[0:8]=='PRODUCT_':
                line=line.strip()
                line=map(string.strip, line.split('='))
                if line[0]=='PRODUCT_UL_CORNER_LAT':uly=float(line[1])
                if line[0]=='PRODUCT_UL_CORNER_LON':ulx=float(line[1])
                if line[0]=='PRODUCT_UR_CORNER_LAT':ury=float(line[1])
                if line[0]=='PRODUCT_UR_CORNER_LON':urx=float(line[1])
                if line[0]=='PRODUCT_LR_CORNER_LAT':lry=float(line[1])
                if line[0]=='PRODUCT_LR_CORNER_LON':lrx=float(line[1])
                if line[0]=='PRODUCT_LL_CORNER_LAT':lly=float(line[1])
                if line[0]=='PRODUCT_LL_CORNER_LON':llx=float(line[1])

        #Geotransform
        ext=[[ulx,uly],[urx,ury],[lrx,lry],[llx,lly],[ulx,uly]]
        ncols=map(int, str(ncols).split(','))
        nrows=map(int, str(nrows).split(','))
        cellx,celly=[],[]
        j=0
        while j < len(ncols):
            gcps=[];i=0
            lr=[[0,0],[ncols[j],0],[ncols[j],nrows[j]],[0,nrows[j]]]
            while i < len(ext)-1: #don't need the last xy pair
                gcp=gdal.GCP()
                gcp.GCPPixel,gcp.GCPLine=lr[i]
                gcp.GCPX,gcp.GCPY=ext[i]
                gcp.Id=str(i)
                gcps.append(gcp)
                i+=1
            j+=1
            geotransform = gdal.GCPsToGeoTransform(gcps)
            x,y=geometry.CellSize(geotransform)
            cellx.append(str(x))
            celly.append(str(abs(y)))
        
        self.metadata['cellx']=','.join(cellx)
        self.metadata['celly']=','.join(celly)

        srs=osr.SpatialReference()
        srs.ImportFromEPSG(4326)
        self.metadata['srs']= srs.ExportToWkt()
        self.metadata['epsg']= 4326
        self.metadata['units']= 'deg'
        
        self.metadata['UL']='%s,%s' % tuple(ext[0])
        self.metadata['UR']='%s,%s' % tuple(ext[1])
        self.metadata['LR']='%s,%s' % tuple(ext[2])
        self.metadata['LL']='%s,%s' % tuple(ext[3])
        
        self.metadata['metadata']='\n'.join(['%s: %s' %(m,hdf_md[m]) for m in hdf_md])

        self.metadata['satellite']='E01'
        self.metadata['level']='L1R'
        self.metadata['filetype'] = gdalDataset.GetDriver().ShortName+'/'+gdalDataset.GetDriver().LongName + ' (%s)' % self.metadata['sensor']
        if self.metadata['sensor']=='ALI':self.metadata['sceneid'] = hdf_md['Scene_Id']
        else:self.metadata['sceneid'] = hdf_md['Scene_ID']
        
        imgdate=time.strptime(hdf_md['ImageStartTime'][0:7], '%Y%j')
        self.metadata['imgdate']=time.strftime('%Y-%m-%d',imgdate)#ISO 8601 
        self.metadata['rotation']=geometry.Rotation(geotransform)
        if abs(self.metadata['rotation']) < 1.0:
            self.metadata['orientation']='Map oriented'
            self.metadata['rotation']=0.0
        else:self.metadata['orientation']='Path oriented'

        self.metadata['filesize']=sum([os.path.getsize(file) for file in filelist])
        self.metadata['filelist']=','.join(utilities.fixSeparators(filelist))
        self.metadata['compressionratio']=0
        self.metadata['compressiontype']='None'
        self.extent=ext
