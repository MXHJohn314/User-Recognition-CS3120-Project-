#SingleInstance, force
#Persistent
#NoEnv ; Recommended for performance and compatibility with future AutoHotkey releases.
doublequote = `"

;~ The csv file will be created in the same directory that you put the script in (default is your Downloads folder)
logdir := A_ScriptDir "\logs.csv"

;~ The windows that we collect data from are all listed in the file named "safeGroupWindows.txt"
safeGroup := "ahk_group safewindows"
file := "safeGroupWindows.txt"
loop read, %file% 
{
  GroupAdd, safeGroup, % A_LoopReadLine  
}

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
    Menu, TRAY, add, About Keylogger, about_handler
    Menu, TRAY, add, Exit, exit_handler
}

;~ Returns a piece of the csv line for this keyevent; a comma-separated set of boolean values that tell us which modifiers were held down at the same time as the keyevent
getMods(){
    return (GetKeyState("RControl", "P") || GetKeyState("LControl", "P")) . ","
    . (GetKeyState("RAlt", "P") || GetKeyState("LAlt", "P")) . ","
    . (GetKeyState("RWin", "P") || GetKeyState("LWin", "P")) . ","
    . (GetKeyState("RShift", "P") || GetKeyState("LShift", "P"))
}

;~ Creates and appends a new record to log.csv for each keystroke.
keyEvent() {
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

;~ This script only collects data from windows that are in the "safeGroupWindows.txt" file
#IfWinActive,ahk_group safeGroup
{
    ;~ This is a list of all the keys we want to capture
    ~*a up::
    ~*a::
    ~*b up::
    ~*b::
    ~*c up::
    ~*c::
    ~*d up::
    ~*d::
    ~*e up::
    ~*e::
    ~*f up::
    ~*f::
    ~*g up::
    ~*g::
    ~*h up::
    ~*h::
    ~*i up::
    ~*i::
    ~*j up::
    ~*j::
    ~*k up::
    ~*k::
    ~*l up::
    ~*l::
    ~*m up::
    ~*m::
    ~*n up::
    ~*n::
    ~*o up::
    ~*o::
    ~*p up::
    ~*p::
    ~*q up::
    ~*q::
    ~*r up::
    ~*r::
    ~*s up::
    ~*s::
    ~*t up::
    ~*t::
    ~*u up::
    ~*u::
    ~*v up::
    ~*v::
    ~*w up::
    ~*w::
    ~*x up::
    ~*x::
    ~*y up::
    ~*y::
    ~*z up::
    ~*z::
    ~*1 up::
    ~*1::
    ~*2 up::
    ~*2::
    ~*3 up::
    ~*3::
    ~*4 up::
    ~*4::
    ~*5 up::
    ~*5::
    ~*6 up::
    ~*6::
    ~*7 up::
    ~*7::
    ~*8 up::
    ~*8::
    ~*9 up::
    ~*9::
    ~*0 up::
    ~*0::
    ~*= up::
    ~*=::
    ~*- up::
    ~*-::
    ~*Tab up::
    ~*Tab::
    ~*CapsLock up::
    ~*CapsLock::
    ~*AppsKey up::
    ~*AppsKey::
    ~*Space up::
    ~*Space::
    ~*BackSpace up::
    ~*BackSpace::
    ~*Delete up::
    ~*Delete::
    ~*PrintScreen up::
    ~*PrintScreen::
    ~*Left up::
    ~*Left::
    ~*Right up::
    ~*Right::
    ~*Up up::
    ~*Up::
    ~*Down up::
    ~*Down::
    ~*Home up::
    ~*Home::
    ~*End up::
    ~*End::
    ~*PGUP up::
    ~*PGUP::
    ~*PGDN up::
    ~*PGDN::
    ~*Insert up::
    ~*Insert::
    ~*Pause up::
    ~*Pause::
    ~*ScrollLock up::
    ~*ScrollLock::
    ~*NumLock up::
    ~*NumLock::
    ~*SC029 up::
    ~*SC029::
    ~*\ up::
    ~*\::
    ~*, up::
    ~*,::
    ~*. up::
    ~*.::
    ~*/ up::
    ~*/::
    ~*' up::
    ~*'::
    ~*[ up::
    ~*[::
    ~*] up::
    ~*]::
    ~*; up::
    ~*;::
    ~*Escape up::
    ~*Escape::
    keyEvent()
    return
}
