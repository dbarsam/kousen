@echo off
rem Backup Current Directory
pushd %~dp0

start ..\.env\Lib\site-packages\PySide\designer.exe 

popd
