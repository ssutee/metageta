@echo off
call setenv.bat

REM Check if the progress bar GUI will be used.
IF /I "%5"=="FALSE" (
call python.exe crawler.py %*
pause
) ELSE (
start "Crawler" /B pythonw.exe crawler.py %*
)
