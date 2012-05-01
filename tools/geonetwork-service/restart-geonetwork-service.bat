@echo off
cd 
C:\Python27\python %~DP0\geonetwork-service.py restart now
rem sc stop geonetwork-service
rem sc start geonetwork-service
pause