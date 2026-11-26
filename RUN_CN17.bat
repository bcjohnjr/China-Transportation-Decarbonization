@echo off
setlocal
cd /d "%~dp0"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
python cn17_validate.py --inputs
if errorlevel 1 goto failed
python cn17_prepare.py
if errorlevel 1 goto failed
python cn17_inventory.py
if errorlevel 1 goto failed
python cn17_evidence.py
if errorlevel 1 goto failed
python cn17_figures.py
if errorlevel 1 goto failed
python cn17_validate.py
if errorlevel 1 goto failed
echo CN v1.7 complete.
exit /b 0
:failed
echo CN v1.7 failed. See the error above.
exit /b 1
