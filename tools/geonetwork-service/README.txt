This script creates a Windows service for GeoNetwork.
Default parameters, are set via a config file - geonetwork-service.ini
The service runs at Windows startup. Messages are written to the Windows Event logs (to view, open "Start->Administrative Tools->Event Viewer" and look in the Applications tab). 
Once installed, the service can be started/stopped via the Services control panel.
This service relies on Python 2.5+ (not 3x) and PyWin32. If Python/PyWin32 is uninstalled, this service will not start. 
If Python/PyWin32 is upgraded and the old version removed, this service will not start, but can be reinstalled by adding the the install directory of the current Python version to the PATH environment variable and rerunning the install script.
If you make changes to the config file, you will need to restart the service.
