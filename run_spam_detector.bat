@echo off
chcp 65001 > nul

REM === Navigate to project directory ===
cd /d "D:\SignalSentinel - Telecom Anomaly Detection System (GxP-Compliant)"

REM === Create logs directory if it doesn't exist ===
if not exist logs mkdir logs

REM === Set timestamp for log file ===
for /f "tokens=1-4 delims=/ " %%a in ('date /t') do (
    set YYYY=%%d
    set MM=%%b
    set DD=%%c
)
for /f "tokens=1-2 delims=: " %%a in ('time /t') do (
    set HH=%%a
    set MIN=%%b
)
set HH=%HH: =0%
set LOGTIME=%YYYY%-%MM%-%DD%_%HH%-%MIN%
set LOGFILE=logs\run_log_%LOGTIME%.txt

REM === Run Python script with optional logtime argument ===
echo [INFO] Starting script at %DATE% %TIME% > %LOGFILE%
python spam_call_anomaly_dual.py --logtime %LOGTIME% >> %LOGFILE% 2>&1

REM === Check for error ===
IF %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Script failed with code %ERRORLEVEL% >> %LOGFILE%
    echo %DATE% %TIME% - [FAIL] Python script crashed >> logs\error_log.txt
    exit /b %ERRORLEVEL%
)

echo [OK] Script completed successfully >> %LOGFILE%
exit /b 0
