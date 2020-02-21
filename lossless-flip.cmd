@echo off
cls
cd %~dp0


:: Queue in Python with:
python lossless-flip.py %*
echo.
::PAUSE