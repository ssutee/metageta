@echo off
call setenv.bat

REM Check if the progress bar GUI will be used.
SET GUI=0
FOR %%A IN (%*) DO (
      IF /I "%%A"=="--gui" SET GUI=1
)

IF /I "%GUI%"=="0" (
call python.exe runcrawler.py %*
pause
) ELSE (
start "Crawler" /B pythonw.exe runcrawler.py %*
)
