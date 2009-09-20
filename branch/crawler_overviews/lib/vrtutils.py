#========================================================================================================
#VRT Utilities
#========================================================================================================
def CreateSimpleVRT(bands,cols,rows,datatype,relativeToVRT=0):
    try:
        vrt=[]
        vrt.append('<VRTDataset rasterXSize="%s" rasterYSize="%s">\n' % (cols,rows))
        for i,band in enumerate(bands):
            vrt.append('  <VRTRasterBand dataType="%s" band="%s">\n' % (datatype, i+1))
            vrt.append('    <SimpleSource>\n')
            vrt.append('      <SourceFilename relativeToVRT="%s">%s</SourceFilename>\n' % (band,relativeToVRT))
            vrt.append('      <SourceBand>1</SourceBand>\n')
            vrt.append('    </SimpleSource>\n')
            vrt.append('  </VRTRasterBand>\n')
        vrt.append('</VRTDataset>\n')
    except:
        return None
    return '\n'.join(vrt)

def CreateRawRasterVRT(bands,cols,rows,datatype,nbits):
    try:
        vrt=[]
        vrt.append('<VRTDataset rasterXSize="%s" rasterYSize="%s">\n' % (cols,rows))
        for i,band in enumerate(bands):
            vrt.append('  <VRTRasterBand dataType="%s" band="%s" subClass="VRTRawRasterBand">\n' % (datatype, i+1))
            vrt.append('    <SourceFilename relativeToVRT="1">%s</SourceFilename>\n' % (band))
            vrt.append('    <PixelOffset>%s</PixelOffset>\n' % (nbits))
            vrt.append('    <LineOffset>%s</LineOffset>\n' % (nbits * cols))
            vrt.append('  </VRTRasterBand>\n')
        vrt.append('</VRTDataset>\n')
    except:
        return None
    return '\n'.join(vrt)

def CreateCustomVRT(vrtxml,vrtcols,vrtrows):
    try:
        vrt=[]
        vrt.append('<VRTDataset rasterXSize="%s" rasterYSize="%s">\n' % (vrtcols,vrtrows))
        vrt.append('%s\n' % vrtxml)
        vrt.append('</VRTDataset>\n')
    except:
        return None
    return '\n'.join(vrt)