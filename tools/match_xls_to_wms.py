import os,shutil
from metageta import utilities

xls=r'C:\WorkSpace\iwsimages.xls'
dbf=r'C:\WorkSpace\wmsextents.xls' #File save-as from dbf
out=r'C:\WorkSpace\iwsimages_updated.xls'

if os.path.exists(out):os.unlink(out)
shutil.copy(xls,out)

#Build a dict of existing records
row=-1
xlsrecs=[]
xlsrows={}
xlsflds=[]
dbfrecs={}

wmstxt='''URL|http://pvac01mult01.internal.govt/ecwp/ecw_wms.dll?
protocol|OGC:WMS-1.1.1-http-get-map
name|%s
description|Image Web Server Web Map Service
function|download'''
ecwtxt='''URL|%s
protocol|WWW:LINK-1.0-http--related
name|ECWP
description|Enhanced Compressed Wavelet Protocol
function|download'''

row=-1
for row,rec in enumerate(utilities.ExcelReader(dbf)):
    fp=rec['FILEPATH'].lower()
    dbfrecs[fp]=rec

row=-1
for row,rec in enumerate(utilities.ExcelReader(xls,list)):
    if row==0:
        xlsflds=[f[0] for f in rec]
        fpi=xlsflds.index('filepath')
        tit=xlsflds.index('title')
        ori=xlsflds.index('OnlineResource') #will only get the first one!
        ExcelWriter=utilities.ExcelWriter(out,xlsflds,update=True)

    fp=rec[fpi][1].lower()
    try:
        dbfrec=dbfrecs[fp]
        if not '?wetlands' in rec[ori] and not '?nautical_charts' in rec[ori]:
            rec[ori]=('OnlineResource', wmstxt%dbfrec['WMSNAME'])
            rec[ori+1]=('OnlineResource', ecwtxt%dbfrec['ECWP'])
            if '_' not in dbfrec['WMSTITLE']:
                rec[tit]=('title', dbfrec['WMSTITLE'])
            ExcelWriter.UpdateRecord(rec,row)
    except KeyError: pass
    except Exception as err:
        print err
        raise

