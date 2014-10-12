@echo off
rem Backup Current Directory
pushd %~dp0

call ..\.env\Scripts\activate.bat

popd
