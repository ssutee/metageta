@echo off
call setenv.bat

call python.exe runtransform.py %*
pause

REM IF /I "%5"=="FALSE" (
REM call python.exe runtransform.py %*
REM pause
REM ) ELSE (
REM start "Crawler" /B python.exe runtransform.py %*
REM )
