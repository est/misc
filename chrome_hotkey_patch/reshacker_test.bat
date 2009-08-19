@echo off
ResHacker.exe -extract chrome.dll, 1.res, 9,, && type ResHacker.log
test.au3
ResHacker.exe -extract 1.res, 1.rc, 9,, && type ResHacker.log
ResHacker.exe -extract 3.res, 3.rc, 9,, && type ResHacker.log