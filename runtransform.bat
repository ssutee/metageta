@echo off
call setenv.bat

IF /I "%5"=="FALSE" (
call python.exe runtransform.py %*
pause
) ELSE (
start "Crawler" /B pythonw.exe runtransform.py %*
)
pause