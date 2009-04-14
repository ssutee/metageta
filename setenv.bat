@echo off 
pushd %~dp0
set CURDIR=%cd%
cd ..
set PARDIR=%cd% 
popd
REM used to use %PARDIR% but I changed the dir structure around.

set OSGEO4W_ROOT=%CURDIR%\OSGeo4W
set PYTHONHOME=%CURDIR%\Python25

PATH=%PYTHONHOME%;%OSGEO4W_ROOT%\bin;%PATH%
for %%f in ("%OSGEO4W_ROOT%\etc\ini\*.bat") do call "%%f"
call "%OSGEO4W_ROOT%\bin\gdal16.bat"

REM Some vars
set PYTHONHOME=%CURDIR%\Python25
SET GDAL_DATA=%CURDIR%\gdal_data
SET PYTHONPATH=%OSGEO4W_ROOT%\bin;%PYTHONHOME%\Lib\lib-tk;%CURDIR%;%PYTHONPATH%
PATH=%GDAL_DRIVER_PATH%;%PATH%
