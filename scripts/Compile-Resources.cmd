@echo off
rem Backup Current Directory
pushd %~dp0

..\.env\Lib\site-packages\PySide\pyside-rcc.exe ..\resources\resources.qrc -o ..\kousen\resources_rc.py -py3

popd
