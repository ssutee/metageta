#Regular expression list of file formats
format_regex=[r'm[oyc]d\w{4,4}\.[0-9]{4,4}\.[0-9]{3,3}\.aust\.[0-9]{3,3}\.b[0-9]{2,2}\..*\.hdf.*'] #CSIRO MODIS

#import base dataset module
import __dataset__

# import other modules (use "_"  prefix to import privately)
import sys, os, re, glob, time, math, string
import utilities
import geometry

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
        """Read Metadata for an CSIRO MODIS format image as GDAL doesn't"""
        #See http://www.cmar.csiro.au/e-print/open/2008/Pagetmj_a.pdf
        #and http://www-data.wron.csiro.au/rs/MODIS/LPDAAC/MODIS_LandData_readme.txt

        #Filename format = MXDxxxx.yyyy.ddd.aust.ccc.bNN.label.hdf.gz
        filelist=[m for m in utilities.rglob(os.path.split(f)[0], r'M[OYC]D\w{4,4}', True, re.IGNORECASE)]
        filelist.sort()
        f=filelist[0] #1st band
        regex='quality|solar_zenith|view_zenith|relative_azimuth|state_flags|day_of_year'
        nbands=0
        bands=[]
        for m in filelist:
            m=(os.path.split(m)[1]).split('.')
            name=m[6]
            if not re.search(regex,name):
                name=' '.join(name.split('_')[1:]).upper() #Strip off cell size
                nbands+=1
                bands.append(name.upper())

        m = self.metadata['filename'].split('.')
        if m[0][1].upper() == 'O':self.metadata['satellite']='Terra'
        elif m[0][1].upper() == 'Y':self.metadata['satellite']='Aqua'
        elif m[0][1].upper() == 'C':self.metadata['satellite']='Combined Terra and Aqua'
        imgdate=time.strptime(m[1]+m[2], '%Y%j')
        self.metadata['imgdate']=time.strftime('%Y-%m-%d',imgdate)#ISO 8601 
        #self.metadata['imgdate']=time.strftime('%Y%m%d',imgdate)
        self.metadata['filesize']=sum([os.path.getsize(file) for file in filelist])
        self.metadata['filelist']=','.join(utilities.fixSeparators(filelist))
        self.metadata['filetype'] = 'HDF-EOS (CSIRO MODIS)'
        self.metadata['metadata'] = ''
        self.metadata['orientation'] = 'Map oriented'
        self.metadata['rotation'] = 0
        self.metadata['nbits'] = 8
        self.metadata['datatype'] = 'Byte'
        self.metadata['nbands'] = nbands
        self.metadata['bands'] = ','.join(bands)
        self.metadata['sensor']='MODIS'
        self.metadata['nodata'] = 0

        px = (m[6].split('_')[0])
        ulx,uly=110.000000,-45.000512
        urx,ury=155.001329,-45.000512
        lrx,lry=155.001329,-10.000000
        llx,lly=110.000000,-10.000000
        if px == '250m':
            self.metadata['cellx'],self.metadata['celly']=0.0023,0.0023
            self.metadata['cols'],self.metadata['rows']=19160,14902
        elif px == '500m':
            self.metadata['cellx'],self.metadata['celly']=0.0047,0.0047
            self.metadata['cols'],self.metadata['rows']=9580,7451
        elif px == '1000m':
            self.metadata['cellx'],self.metadata['celly']=0.0094,0.0094
            self.metadata['cols'],self.metadata['rows']=4790,3726
            uly,ury=-45.005209

        self.metadata['UL']='%s,%s' % tuple([ulx,uly])
        self.metadata['UR']='%s,%s' % tuple([urx,ury])
        self.metadata['LR']='%s,%s' % tuple([lrx,lry])
        self.metadata['LL']='%s,%s' % tuple([llx,lly])
        src_srs=osr.SpatialReference()
        src_srs.ImportFromEPSG(4326)
        self.metadata['srs']= src_srs.ExportToWkt()
        self.metadata['epsg']= '4326'
        self.metadata['units'] = 'deg'

        if re.search(r'\.gz$', self.metadata['filename'], re.I):
            self.metadata['metadata'] = 'Compression ratio derived from all associated files\nincluding metadata files'
            self.metadata['compressionratio']=int((self.metadata['nbands']*self.metadata['cols']*self.metadata['rows']*(self.metadata['nbits']/8.0))/self.metadata['filesize'])
            self.metadata['compressiontype']='GZIP'
        else:
            self.metadata['compressionratio']=0
            self.metadata['compressiontype']='None'

        self.extent=[[ulx,uly],[urx,ury],[lrx,lry],[llx,lly],[ulx,uly]]
