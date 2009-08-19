opt("GUIOnEventMode", 1)

; "reshacker.exe -modify chrome.dll, chromenew.dll, test.rc, ACCELERATOR,101,"
; Use FileInstall() or http://www.autoitscript.com/forum/index.php?showtopic=51103

$help_text = "F1 Undo close tab	F2 Previous tab" & @CRLF & "F3 Next tab		F4 Close tab"


$Form1 = GUICreate("Chrome Hotkey Patch", 386, 126, 206, 206)
GUISetOnEvent(-3, "Close")
GUISetIcon("icon.ico")

$Button1 = GUICtrlCreateButton("&Patch!", 304, 8, 75, 25, 0)
GUICtrlSetOnEvent(-1, "Button1_OnClick")

$t = "chrome.dll"
If $CmdLine[0]==1 Then
  $t = $CmdLine[1]
EndIf
$Input1 = GUICtrlCreateInput($t, 8, 8, 209, 21)

$Button2 = GUICtrlCreateButton("&Browse", 224, 8, 75, 25, 0)
GUICtrlSetOnEvent(-1, "Button2_OnClick")

$Label1 = GUICtrlCreateLabel("Google Chrome browser Hotkey Patch" & @CRLF & "By est, electronicstar@126.com" & @CRLF & "http://initiative.yo2.cn/" & @CRLF & $help_text, 8, 40, 370, 75)
GUICtrlSetFont(-1, 9, 400, 0, "Courier New")
GUICtrlSetOnEvent(-1, "Label1_OnClick")

GUISetState(@SW_SHOW)


While 1
    Sleep(1000)
WEnd


; modify chrome.dll and save it
Func Button1_OnClick()
  $chromedll = GUICtrlRead($Input1)
  If StringMid($chromedll, 2, 1) <> ":" Then $chromedll = @WorkingDir & "\" & $chromedll
  FileChangeDir(@TempDir)
  FileInstall("ResHacker.exe", @TempDir & "\ResHacker.exe", 1)
  If FileExists ($chromedll) Then
    $size1 = FileGetSize($chromedll)    
    
    RunWait ("ResHacker.exe -extract """ & $chromedll &""", fuckgfw.res, ACCELERATORS,101,")

    FileMove($chromedll, $chromedll & ".bak")
    
    $file1 = FileOpen("fuckgfw.res", 16)
    $c = FileRead($file1)
    FileClose($file1)


    $h = String($c)
    $l1 = StringLen($h)


    $body_len = Dec(StringRegExpReplace(StringMid($h, 67, 8), "([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})", "${4}${3}${2}${1}"))


    ;modify hotkeys
    ;http://msdn.microsoft.com/en-us/library/ms927178.aspx
    ;http://msdn.microsoft.com/en-us/library/ms648007(VS.85,loband).aspx
    
    ; F1 to Ctrl+F1
    $h = StringRegExpReplace($h, "0100(7000[0-9A-F]{4}0000)", "0900${1}")
    ; VK_F2 71, VK_F3 72, VK_F4 73 to nothing
    $h = StringRegExpReplace($h, "01007100[0-9A-F]{4}0000", "")
    $h = StringRegExpReplace($h, "01007200[0-9A-F]{4}0000", "")
    $h = StringRegExpReplace($h, "01007300[0-9A-F]{4}0000", "")
    ; Ctrl+Shift+T to F1
    $h = StringRegExpReplace($h, "0D005400([0-9A-F]{4}0000)", "0D005400${1}01007000${1}")
    ; Ctrl+Shift+Tab to F2
    $h = StringRegExpReplace($h, "0D000900([0-9A-F]{4}0000)", "0D000900${1}01007100${1}")
    ; Ctrl+Tab to F3
    $h = StringRegExpReplace($h, "09000900([0-9A-F]{4}0000)", "09000900${1}01007200${1}")
    ; Ctrl+W to F4
    $h = StringRegExpReplace($h, "09007300([0-9A-F]{4}0000)", "09007300${1}01007300${1}")

    $l2 = StringLen($h)
    $delta = ($l2 - $l1 ) / 2
    $body_len += $delta
    $body_len_hex = StringRegExpReplace(Hex($body_len), "([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})([0-9A-F]{2})", "${4}${3}${2}${1}")
    
    $h = StringReplace($h, 67, $body_len_hex)

    $file2 = FileOpen("gfwCNM.res", 18)
    FileWrite($file2, Binary($h))
    FileClose($file2)
    
    
    RunWait ("reshacker.exe -addoverwrite """ & $chromedll & ".bak"", """ & $chromedll & """, gfwCNM.res, ACCELERATORS,101,")
    
    $size2 = FileGetSize($chromedll & ".bak")
        
    GUICtrlSetData($Label1, "Patch completed & have fun!" & @CRLF & "New chrome.dll size:" & $size2 & " bytes" & @CRLF & "Backup chrome.dll.bak size: " & $size1 & " bytes" & @CRLF & $help_text)
    
  Else
    Button2_OnClick()
    Button1_OnClick()
  EndIf
EndFunc


; Browse for chrome.dll
Func Button2_OnClick()
  $chromedll = FileOpenDialog ("Select chrome.dll", ".", "Chrome.dll (chrome.dll)")
  If @error==1 Then
    $chromedll = "chrome.dll"
  EndIf
  GUICtrlSetData($Input1, $chromedll)
EndFunc

Func Label1_OnClick()
  ShellExecute ("http://initiative.yo2.cn/")
EndFunc


Func Close()
  FileDelete("fuckgfw.res")
  FileDelete("gfwCNM.res")
  FileDelete("ResHacker.*")
  Exit
EndFunc