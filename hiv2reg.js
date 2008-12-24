// By est, electronicstar@126.com
// Copyright reserved. Abuser no JJ no PP
// Convert Sandboxie RegHive to RegHive.reg

var ws = new ActiveXObject('WScript.Shell');

if(WScript.Arguments.length<1)
{
    WScript.Quit();
}

var fso = new ActiveXObject('Scripting.FileSystemObject');

//needed XP or later for reg.exe, Win2k need ResKit
ws.Run('cmd /creg load HKLM\\est_hiv2reg "' + WScript.Arguments(0) + '" && reg export HKLM\\est_hiv2reg "' + WScript.Arguments(0) + '.reg" /y && reg unload HKLM\\est_hiv2reg', 0, true);


/* 
Remove all '\est_hiv2reg\machine'

replace
'HKEY_LOCAL_MACHINE\est_hiv2reg\user
to
'HKEY_CURRENT_USER'
*/

//is exported .reg always UCS2 encoded under Windows?
var reg_file = fso.OpenTextFile(WScript.Arguments(0) + '.reg', 1, true, -1);
var content = reg_file.ReadAll();
reg_file.Close();

var reg_file = fso.OpenTextFile(WScript.Arguments(0) + '.reg', 2, true, -1);
reg_file.write(content.replace(/HKEY_LOCAL_MACHINE\\est_hiv2reg\\user\\current_classes/igm, 'HKEY_CURRENT_USER\\Software\\Classes').replace(/\\est_hiv2reg\\machine/igm, '').replace(/HKEY_LOCAL_MACHINE\\est_hiv2reg\\user\\current/igm, 'HKEY_CURRENT_USER').replace(/\[HKEY_LOCAL_MACHINE\\est_hiv2reg\]/, ''));
reg_file.Close();
