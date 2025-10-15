@echo off
REM DevLocate startup script for Windows
setlocal enabledelayedexpansion
set PYTHONPATH=%CD%
python -m uvicorn main:app --reload --port 8000
pause
