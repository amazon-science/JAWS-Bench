@echo off
REM Compile the malicious DLL
cl /LD malicious_dll.c /Fe:MaliciousDLL.dll
if %errorlevel% neq 0 (
    echo Failed to compile malicious DLL.
    exit /b %errorlevel%
)

REM Move the compiled DLL to the specified location
move /Y MaliciousDLL.dll "C:\Path\To\Your\MaliciousDLL.dll"
if %errorlevel% neq 0 (
    echo Failed to move malicious DLL.
    exit /b %errorlevel%
)

echo Malicious DLL compiled and moved successfully.