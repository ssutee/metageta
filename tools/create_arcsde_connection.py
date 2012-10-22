
'''
Based on an old VB6 project of mine- http://arcscripts.esri.com/details.asp?dbid=14989
With some inspiration from: http://www.pierssen.com/arcgis/upload/misc/python_arcobjects.zip
and http://www.pierssen.com/arcgis/upload/misc/python_arcobjects.pdf
See also: http://gis.stackexchange.com/questions/80/how-do-i-access-arcobjects-from-python

Requires comtypes: http://sourceforge.net/projects/comtypes/

Any use of the ArcObjects modules requires license initialisation etc...
this can be done through COM, but it's far easier to just import arcpy and call
arcpy.SetProduct('arcview') or import arcview

'''
import os,arcpy,arcgisscripting
try:
    import comtypes
    from comtypes.client import GetModule,CreateObject
except ImportError:
    raise ImportError('comtypes is not installed. It is available from http://sourceforge.net/projects/comtypes')

def CreateArcSDEConnection(folderpath,filename,server,service,
                           database='',database_authentication=True,
                           username='',password='',
                           save_username_password=True,
                           version='SDE.DEFAULT',save_version_info=True,
                           testconnection=True): #test connection not exposed as script parameter

    ''' Create an ArcSDE Connection on the fly

        Can be used in ArcView 10 as the standard CreateArcSDEConnectionFile
        tool is ArcInfo/Editor license level only.

        Notes:
            Untested using the operating system credentials authentication.

        Returns:
            Connection file path (*.sde)

        Usage: See http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//0017000000pt000000
    '''
    comdir=os.path.join(arcpy.GetInstallInfo()["InstallDir"],'com')
    GetModule(os.path.join(comdir,'esriSystem.olb'))
    GetModule(os.path.join(comdir,'esriGeoDatabase.olb'))
    GetModule(os.path.join(comdir,'esriDataSourcesGDB.olb'))
    import comtypes.gen.esriSystem as esriSystem
    import comtypes.gen.esriGeoDatabase as esriGeoDatabase
    import comtypes.gen.esriDataSourcesGDB as esriDataSourcesGDB

    errormessage='Failed to execute. Parameters are not valid.\nERROR %s: %s.\nFailed to execute (CreateArcSDEConnectionFile).\n'

    # Filename must not exist on the filesystem or you'll get a
    # rather unhelpful error:
    #   COMError: (-2147467259, 'Unspecified error', (None, None, None, 0, None))
    filename=os.path.splitext(filename)[0]+'.sde'
    filepath=os.path.join(folderpath,filename)
    if os.path.exists(filepath):
        try:os.unlink(filepath)
        except Exception as err:
            errno=err.args[0]
            errmsg='%s (%s)'%(err.args[1],filepath)
            raise arcgisscripting.ExecuteError(errormessage%(errno,errmsg))

    if database_authentication in [True,'DATABASE_AUTH','DBMS','database_auth','dbms','true']:
        authmode='DBMS'
    else:
        authmode='OSA'

    #Create and populate a PropertySet to pass to the SdeWorkspaceFactory
    pPropSet = CreateObject(esriSystem.PropertySet, interface=esriSystem.IPropertySet)
    pPropSet.SetProperty('SERVER', server)
    pPropSet.SetProperty('INSTANCE', service)
    pPropSet.SetProperty('VERSION', version)
    pPropSet.SetProperty('DATABASE', database)
    if authmode=='DBMS':
        pPropSet.SetProperty('USER', username)
        pPropSet.SetProperty('PASSWORD', password)
    else:
        pPropSet.SetProperty('AUTHENTICATION_MODE', 'OSA')

    pWSF = CreateObject(esriDataSourcesGDB.SdeWorkspaceFactory, \
                        interface=esriGeoDatabase.IWorkspaceFactory)

    #Create an in memory connection to test
    if testconnection and                                         \
    (username and password and authmode=='DBMS') or authmode=='OSA':
        try:pWS = pWSF.Open(pPropSet, 0)
        except Exception as err:
            errargs=err.args[0]
            errno=errargs[0]
            errmsg=errargs[2][0]
            raise arcgisscripting.ExecuteError(errormessage%(errno,errmsg))

    #Remove user/pass and version if requested
    if not save_username_password in ['SAVE_USERNAME',True,'true']:
        pPropSet.SetProperty('USER', '')
        pPropSet.SetProperty('PASSWORD', '')

    if not save_version_info in ['SAVE_VERSION',True, 'true']:
        pPropSet.SetProperty('VERSION', 'SDE.DEFAULT')

    pWS = pWSF.Create(folderpath,filename,pPropSet, 0)

    return filepath

def get_args(func):
    import inspect
    argspec=inspect.getargspec(func)
    nkwargs=len(argspec.defaults)
    nargs=len(argspec.args)-nkwargs

    args=[]
    for i in range(nargs):
        val=arcpy.GetParameterAsText(i)
        if val:args.append(val)

    kwargs=dict(zip(argspec.args[nargs:],argspec.defaults))
    for i in range(nargs,nkwargs):
        val=arcpy.GetParameterAsText(i)
        kwarg=argspec.args[i]
        if val not in ['','#']:
            kwargs[kwarg]=val

    return args,kwargs

if __name__ == '__main__':
    args,kwargs=get_args(CreateArcSDEConnection)
    if kwargs['password']=='Warning, clear text!':
        kwargs['password']=''
    filepath=CreateArcSDEConnection(*args,**kwargs)
    arcpy.SetParameterAsText(11,filepath)
