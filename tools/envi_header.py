import re

def get_envi_header_dict(hdr):
    #Get all "key = {val}" type matches
    regex=re.compile(r'^(.+?)\s*=\s*({\s*.*?\n*.*?})$',re.M|re.I)
    matches=regex.findall(hdr)

    #Remove them from the header
    subhdr=regex.sub('',hdr)

    #Get all "key = val" type matches
    regex=re.compile(r'^(.+?)\s*=\s*(.*?)$',re.M|re.I)
    matches.extend(regex.findall(subhdr))

    return dict(matches)

if __name__=='__main__':
    hdr='''ENVI
description = {
  RPC Orthorectification Result [Mon Aug 13 13:38:09 2012] [Mon Aug 13
  13:38:09 2012]}
samples = 27856
lines   = 30016
bands   = 1
header offset = 0
file type = ENVI Standard
data type = 12
interleave = bsq
sensor type = WorldView
byte order = 0
map info = {UTM, 1.000, 1.000, 723000.000, 8129434.000, 5.0000000000e-001, 5.0000000000e-001, 55, South, WGS-84, units=Meters}
coordinate system string = {PROJCS["UTM_Zone_55S",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",10000000.0],PARAMETER["Central_Meridian",147.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]}
wavelength units = Micrometers
band names = {
 Orthorectified (Band 1)}
wavelength = {
 0.625000}
'''
    print get_envi_header_dict(hdr)