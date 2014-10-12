@echo off
rem Backup Current Directory
pushd %~dp0

start ..\.env\Lib\site-packages\PySide-1.2.2-py3.3-win32.egg\PySide\designer.exe 

popd
