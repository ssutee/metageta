@echo off
call "%~DP0setenv.bat"

REM Check if the progress bar GUI will be used.
set gui=0
set /a nargs=0
for %%a in (%*) do (
    set /a nargs+=1
    if /i "%%a"=="--gui" set gui=1
)
if %nargs%==0 set gui=1
if /i "%gui%"=="0" (
    call python.exe "%~DP0runcrawler.py" %*
    pause
) else (
    REM Not using the GUI until I sort out the disconnection bug
    REM call python.exe  "%~DP0runcrawler.py" %* 
    REM pause
    start "Crawler" /b pythonw.exe "%~DP0runcrawler.py" --gui %*
)