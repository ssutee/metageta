@echo off
C:\Python27\python %~DP0\geonetwork-service.py --startup auto install
C:\Python27\python %~DP0\geonetwork-service.py start
pause