@echo off
:By est, electroniXtar@Gmail.com
if [%1]==[] (
    echo Usage: %0 data1.hdr
    goto:eof
)
set ISCAB=%~dp0ISCAB.exe
md %~dpn1
pushd %~dpn1
%ISCAB% "%~f1" -i"%~dpn1.ini" -l
SETLOCAL ENABLEDELAYEDEXPANSION
for /f "tokens=1* delims==" %%a in ('findstr /r "File[0-9]*" %~dpn1.ini') do (
    if not !LastDir! == %%~dpb (
        md %%~dpb
        set LastDir=%%~dpb
    )
)
ENDLOCAL
%ISCAB% "%~f1" -i"%~dpn1.ini" -x
popd