@echo off
python geonetwork-service.py --startup auto install
python geonetwork-service.py start
rem pause