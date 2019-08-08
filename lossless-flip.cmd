@echo off
cls
cd %~dp0
python lossless-flip.py %1
EXIT

::	TO DEBUG:
::	Swap 'EXIT' above for 'PAUSE' and change shortcut
::	in 'shell:startup' from "Minimized" to "Maximized"