@echo off
call setenv.bat

IF /I "%5"=="FALSE" (
call python.exe transform.py %*
pause
) ELSE (
call python.exe transform.py %*
REM start "Crawler" /B pythonw.exe transform.py %*
)
