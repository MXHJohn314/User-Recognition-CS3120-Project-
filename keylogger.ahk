#SingleInstance, force
#Persistent
#NoEnv ; Recommended for performance and compatibility with future AutoHotkey releases.
doublequote = `"

;~ The csv file will be created in the same directory that you put the script in (default is your Downloads folder)
logdir := A_ScriptDir "\logs.csv"

;~ This creates the column headers for the outputted csv file
if(!fileexist(logdir)) {
    FileAppend,% "month,day,hour,minute,millis,isDown,ctrl,alt,win,shift,key`n", %logdir%
}
make_menu()
return

;~ A user-friendly icon on the task bar, for your convenience
make_menu() {
    Menu, TRAY, NoStandard
    Menu, TRAY, add, YOU ARE BEING LOGGED - help, help_handler
    Menu, TRAY, add,
    Menu, TRAY, add, Start new logfile, newlog_handler
    Menu, TRAY, add, About Keylogger, about_handler
    Menu, TRAY, add, Exit, exit_handler
}

getMods(){
    return (GetKeyState("RControl", "P") || GetKeyState("LControl", "P")) . ","
    . (GetKeyState("RAlt", "P") || GetKeyState("LAlt", "P")) . ","
    . (GetKeyState("RWin", "P") || GetKeyState("LWin", "P")) . ","
    . (GetKeyState("RShift", "P") || GetKeyState("LShift", "P"))
}

keyevent() {
    global logdir
    isDown := !InStr(A_ThisHotkey, " Up")
    key := SubStr(StrSplit(A_ThisHotkey, " ")[1], 3)
    hk_off := A_ThisHotkey
    hk_on := isDown ?  A_ThisHotkey " Up" : StrSplit(A_ThisHotkey, " ")[1]
    Hotkey, %hk_off%, off
    Hotkey, %hk_on%, on
    row := A_MM "," A_dd "," A_Hour "," A_Min "," A_MSec "," isDown "," getMods() "," key "`n"
    FileAppend, %row%, %logdir%
}

;~ Todo: implement making separate logs

newlog_handler:
return

;~ Right-click this script's icon and select 'About' to read this
about_handler:
MsgBox % "This program is intended for use with machine learning projects.`n"
        . "You are licensed to use it for capturing your own keystrokes."
return

;~ Right-click this script's icon and select 'Exit' to quit reading keystrokes
exit_handler:
ExitApp
return

;~ Right-click this script's icon and select 'Help' to view the current directory where your csv file will be
help_handler:
MsgBox % "All of your key presses are being logged to:`n" logdir
return
safeGroup := "ahk_group safewindows"
;~ ahk_exe idea64.exe
;~ #IfWinActive ahk_exe notepad.exe
;~ #IfWinActive ahk_exe notepad++.exe
;~ #IfWinActive ahk_exe Code.exe
;~ #IfWinActive ahk_exe WINWORD.EXE
;~ #IfWinActive ahk_exe sublime_text.exe

safeWindows := ["ahk_exe idea64.exe"
, "ahk_exe notepad.exe"
, "ahk_exe notepad++.exe"
, "ahk_exe Code.exe"
,"ahk_exe WINWORD.EXE"
,"ahk_exe sublime_text.exe"]

for key, val in  safeWindows {
    GroupAdd, safeGroup,% val
}

#IfWinActive,ahk_group safeGroup
{
    ;~ This is a list of all the keys we want to capture
    ~*a up::keyevent()
    ~*a::keyevent()
    ~*b up::keyevent()
    ~*b::keyevent()
    ~*c up::keyevent()
    ~*c::keyevent()
    ~*d up::keyevent()
    ~*d::keyevent()
    ~*e up::keyevent()
    ~*e::keyevent()
    ~*f up::keyevent()
    ~*f::keyevent()
    ~*g up::keyevent()
    ~*g::keyevent()
    ~*h up::keyevent()
    ~*h::keyevent()
    ~*i up::keyevent()
    ~*i::keyevent()
    ~*j up::keyevent()
    ~*j::keyevent()
    ~*k up::keyevent()
    ~*k::keyevent()
    ~*l up::keyevent()
    ~*l::keyevent()
    ~*m up::keyevent()
    ~*m::keyevent()
    ~*n up::keyevent()
    ~*n::keyevent()
    ~*o up::keyevent()
    ~*o::keyevent()
    ~*p up::keyevent()
    ~*p::keyevent()
    ~*q up::keyevent()
    ~*q::keyevent()
    ~*r up::keyevent()
    ~*r::keyevent()
    ~*s up::keyevent()
    ~*s::keyevent()
    ~*t up::keyevent()
    ~*t::keyevent()
    ~*u up::keyevent()
    ~*u::keyevent()
    ~*v up::keyevent()
    ~*v::keyevent()
    ~*w up::keyevent()
    ~*w::keyevent()
    ~*x up::keyevent()
    ~*x::keyevent()
    ~*y up::keyevent()
    ~*y::keyevent()
    ~*z up::keyevent()
    ~*z::keyevent()
    ~*1 up::keyevent()
    ~*1::keyevent()
    ~*2 up::keyevent()
    ~*2::keyevent()
    ~*3 up::keyevent()
    ~*3::keyevent()
    ~*4 up::keyevent()
    ~*4::keyevent()
    ~*5 up::keyevent()
    ~*5::keyevent()
    ~*6 up::keyevent()
    ~*6::keyevent()
    ~*7 up::keyevent()
    ~*7::keyevent()
    ~*8 up::keyevent()
    ~*8::keyevent()
    ~*9 up::keyevent()
    ~*9::keyevent()
    ~*0 up::keyevent()
    ~*0::keyevent()
    ~*= up::keyevent()
    ~*=::keyevent()
    ~*- up::keyevent()
    ~*-::keyevent()
    ~*Tab up::keyevent()
    ~*Tab::keyevent()
    ~*CapsLock up::keyevent()
    ~*CapsLock::keyevent()
    ~*AppsKey up::keyevent()
    ~*AppsKey::keyevent()
    ~*Space up::keyevent()
    ~*Space::keyevent()
    ~*BackSpace up::keyevent()
    ~*BackSpace::keyevent()
    ~*Delete up::keyevent()
    ~*Delete::keyevent()
    ~*PrintScreen up::keyevent()
    ~*PrintScreen::keyevent()
    ~*Left up::keyevent()
    ~*Left::keyevent()
    ~*Right up::keyevent()
    ~*Right::keyevent()
    ~*Up up::keyevent()
    ~*Up::keyevent()
    ~*Down up::keyevent()
    ~*Down::keyevent()
    ~*Home up::keyevent()
    ~*Home::keyevent()
    ~*End up::keyevent()
    ~*End::keyevent()
    ~*PGUP up::keyevent()
    ~*PGUP::keyevent()
    ~*PGDN up::keyevent()
    ~*PGDN::keyevent()
    ~*Insert up::keyevent()
    ~*Insert::keyevent()
    ~*Pause up::keyevent()
    ~*Pause::keyevent()
    ~*ScrollLock up::keyevent()
    ~*ScrollLock::keyevent()
    ~*NumLock up::keyevent()
    ~*NumLock::keyevent()
    ~*SC029 up::keyevent()
    ~*SC029::keyevent()
    ~*\ up::keyevent()
    ~*\::keyevent()
    ~*, up::keyevent()
    ~*,::keyevent()
    ~*. up::keyevent()
    ~*.::keyevent()
    ~*/ up::keyevent()
    ~*/::keyevent()
    ~*' up::keyevent()
    ~*'::keyevent()
    ~*[ up::keyevent()
    ~*[::keyevent()
    ~*] up::keyevent()
    ~*]::keyevent()
    ~*; up::keyevent()
    ~*;::keyevent()
    ~*Escape up::keyevent()
    ~*Escape::keyevent()
}
