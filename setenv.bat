@echo off 
pushd %~dp0
set CURDIR=%cd%
popd
:: used to use %PARDIR% but I changed the dir structure around.
set OSGEO4W_ROOT=%CURDIR%\OSGeo4W
set PYTHONHOME=%CURDIR%\Python25

:: Initialise OSGEO4W
PATH=%PYTHONHOME%;%OSGEO4W_ROOT%\bin;%PATH%
for %%f in ("%OSGEO4W_ROOT%\etc\ini\*.bat") do call "%%f"
call "%OSGEO4W_ROOT%\bin\gdal16.bat"

:: Some vars
::PYTHONHOME needs to be reset after initialising OSGEO4W
set PYTHONHOME=%CURDIR%\Python25
SET GDAL_DATA=%CURDIR%\gdal_data
SET PYTHONPATH=%OSGEO4W_ROOT%\bin;%PYTHONHOME%\Lib\lib-tk;%CURDIR%\lib;%PYTHONPATH%
PATH=%GDAL_DRIVER_PATH%;%PATH%
