@echo off
title Distributed File Sharing - Storage Servers
cd /d "%~dp0"
start "Storage Server 8001 - IT replica" cmd /k python storage_server.py 8001
start "Storage Server 8002 - Finance replica" cmd /k python storage_server.py 8002
start "Storage Server 8003 - Administration replica" cmd /k python storage_server.py 8003
echo.
echo Three storage server windows have been opened.
echo Now open another Command Prompt in this folder and run:
echo python coordinator.py
echo.
pause
