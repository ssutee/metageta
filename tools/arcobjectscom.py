#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2011 Australian Government, Department of Sustainability, Environment, Water, Population and Communities
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

'''     Beginnings of a module to work with ArcObjects

        Based on python code from: http://www.pierssen.com/arcgis/upload/misc/python_arcobjects.zip and http://www.pierssen.com/arcgis/upload/misc/python_arcobjects.pdf
        Also on an old VB6 project of mine - http://arcscripts.esri.com/details.asp?dbid=14989
        See also: http://gis.stackexchange.com/questions/80/how-do-i-access-arcobjects-from-python

        Requires comtypes: http://sourceforge.net/projects/comtypes/

        Any use of the ArcObjects modules requires license initialisation etc...
        this can be done through COM, see the "InitStandalone()" function in the
        first link above, but it's far easier to just import arcpy/arcgisscripting
        and .SetProduct('arcview')

        Not really sure if it'll go any further than this, the main goal was creating on-the-fly
        ArcSDE connections that could be used in ArcView 10 as the standard CreateArcSDEConnectionFile
        tool is ArcEditor+ license level only.

        Apologies for the camelCase, but "A Foolish Consistency is the Hobgoblin of Little Minds"...

        Luke Pinner 2012

'''
import comtypes,os

def CreateArcSDEConnection(username,password,server,port,
                           version="SDE.DEFAULT",database="",
                           filepath=""):
    ''' Create an ArcSDE Connection on the fly

        Can be used in ArcView 10 as the standard CreateArcSDEConnectionFile
        tool is ArcInfo license level only.

        Can possibly (but untested) be used in 9.x as well

        Notes:
            Limited to username/password currently, though it's possible to
            use pPropSet.SetProperty("AUTHENTICATION_MODE", "OSA") instead to
            use the operating system credentials directly if your DB supports it.

            Filename must not exist on the filesystem or you'll get a
            rather unhelpful error:
                COMError: (-2147467259, 'Unspecified error', (None, None, None, 0, None))

            If filename is an empty string (default) or "IN_MEMORY", an in memory
            workspace is returned. However, I haven't actually figured out how
            to use it... :)

        Returns: Workspace COM object
    '''

    GetModule('esriSystem.olb')
    GetModule('esriGeoDatabase.olb')
    GetModule('esriDataSourcesGDB.olb')
    import comtypes.gen.esriSystem as esriSystem
    import comtypes.gen.esriGeoDatabase as esriGeoDatabase
    import comtypes.gen.esriDataSourcesGDB as esriDataSourcesGDB

    pPropSet = CreateObject(esriSystem.PropertySet, esriSystem.IPropertySet)
    pPropSet.SetProperty("USER", username)
    pPropSet.SetProperty("PASSWORD", password)
    pPropSet.SetProperty("SERVER", server)
    pPropSet.SetProperty("INSTANCE", port)
    pPropSet.SetProperty("VERSION", version)
    pPropSet.SetProperty("DATABASE", database)

    pWSF = CreateObject(esriDataSourcesGDB.SdeWorkspaceFactory, \
                  esriGeoDatabase.IWorkspaceFactory)

    #If filepath is empty, create an in memory connection
    if filepath and filepath.upper()!="IN_MEMORY":
        path,name=os.path.split(filepath)
        pWS = pWSF.Create(path,name,pPropSet, 0)
    else:
        pWS = pWSF.Open(pPropSet, 0)

    return pWS

def SetProduct(product):
    """Init standalone ArcGIS license"""
    GetModule('esriSystem.olb')
    import comtypes.gen.esriSystem as esriSystem

    products={'arcview':esriSystem.esriLicenseProductCodeArcView,
              'arceditor':esriSystem.esriLicenseProductCodeArcEditor,
              'arcinfo':esriSystem.esriLicenseProductCodeArcInfo}

    pInit = CreateObject(esriSystem.AoInitialize,esriSystem.IAoInitialize)
    pCode=products.get(product.lower())
    if pCode:
        licenseStatus = pInit.IsProductCodeAvailable(pCode)
        if licenseStatus == esriSystem.esriLicenseAvailable:
            licenseStatus = pInit.Initialize(pCode)
            return (licenseStatus == esriSystem.esriLicenseCheckedOut)

def InitStandalone():
    """Init standalone ArcGIS license"""
    GetModule('esriSystem.olb')
    import comtypes.gen.esriSystem as esriSystem
    pInit = CreateObject(esriSystem.AoInitialize, \
                   esriSystem.IAoInitialize)
    ProductList = [esriSystem.esriLicenseProductCodeArcEditor, \
                   esriSystem.esriLicenseProductCodeArcView]
    for eProduct in ProductList:
        licenseStatus = pInit.IsProductCodeAvailable(eProduct)
        if licenseStatus != esriSystem.esriLicenseAvailable:
            continue
        licenseStatus = pInit.Initialize(eProduct)
        return (licenseStatus == esriSystem.esriLicenseCheckedOut)
    return False

def GetLibPath():
    """ Get the ArcObjects library path

        It would be nice to just load the module directly instead of needing the path,
        they are registered after all... But I just don't know enough about COM to do this

    """
    import _winreg
    #Little kludge for 64bit OS
    if 'PROGRAMFILES(X86)' in os.environ:path='SOFTWARE\\Wow6432Node\\ESRI'
    else:path='SOFTWARE\\ESRI'
    keyESRI = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, path)

    #Little kludge juuust in case ArcGIS 10.1 uses a different registry key,
    #i.e. "Desktop10.1"...
    i=0
    while 1:
        subkey='ArcGIS'#used in 9.x
        try:
            subkey=_winreg.EnumKey(keyESRI,i)
            if subkey[:7].lower()=='desktop':break
        except:break
        i+=1

    keyESRI = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, path+'\\'+subkey)
    return  os.path.join(_winreg.QueryValueEx(keyESRI,"InstallDir")[0],'com')

def GetModule(sModuleName):
    """ Generate (if not already done) wrappers for COM modules
    """
    from comtypes.client import GetModule
    sLibPath = GetLibPath()
    GetModule(os.path.join(sLibPath,sModuleName))

def CreateObject(COMClass, COMInterface):
    """ Creates a new comtypes POINTER object where
        COMClass is the class to be instantiated,
        COMInterface is the interface to be assigned
    """
    ptr = comtypes.client.CreateObject(COMClass, interface=COMInterface)
    return ptr

def CType(obj, interface):
    """Casts obj to interface and returns comtypes POINTER or None"""
    try:
        newobj = obj.QueryInterface(interface)
        return newobj
    except:pass

if __name__=='__main__':
    #testing...
    import arcpy
    arcpy.SetProduct('arcview')
    filepath='c:/temp/testing123.sde'
    if os.path.exists(filepath):os.unlink(filepath)

    sdecon_file=CreateArcSDEConnection('someuser', 'somepassword',
                                       'someserver','5152',
                                        filepath=filepath)
    arcpy.env.workspace=filepath
    print arcpy.ListFeatureClasses()
    del filepath

