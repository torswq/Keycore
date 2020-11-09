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

'''Module containing general utilities. This includes


    - colorprint: Print in colours
    - kbhit_enter: A function that prints the text
                   "Press enter to continue..."
                   '''


__author__ = 'Aitor Santoro <torsw@protonmail.com>'
__version__ = '1.0'
__license__ = 'LGPLv3'


import os
import sys

def colorprint(text, color='none', effect='none', end='\n', DEBUG = False):
    '''
Description
-----------
    Print the desired colour in terminal

Parameters
----------
text: string
    The text to colour.
    
colour: string
    * 'default' - Default colour
    * 'green' - 'red' - 'yellow' - 'cyan'

Return
------
    Returns the parameter 'text' coloured.
    '''
        # * Error check
    if DEBUG:
        for color in COLORS:
            print(COLORS[color]+f'{color}')
        for effect in EFFECTS:
            print(EFFECTS[effect]+f'{effect}')
        print(EFFECTS['default'])
        return
    if type(text) != type(''):
        print(f"Colorprint message\nInvalid type: '{type(text)}' for the text")
    elif not color in list(COLORS.keys()):
        print(f"Colorprint message\nInvalid color: '{color}'")
    else:
        pass
    string = f"{COLORS[color]}{EFFECTS[effect]}{text}{COLORS['default']}"
    print(string, end=end)
    return string
   

def kbhit_enter():
    '''Prompts a "Press enter to continue".'''
    colorprint(' [DEBUG]: Press enter to continue', 'yellow')
    input()

def _check_termvirt():

    '''Checks for VirtualTerminalLevel windows registry key.'''
    import winreg

    HKEYCU = winreg.HKEY_CURRENT_USER
    KEY_NAME = "Console"
    VALUE_NAME = "VirtualTerminalLevel"
    FULL_KEY = f"HKEY_CURRENT_USER\\{KEY_NAME}\\{VALUE_NAME}"
    DWORD_VALUE = 0x00000001
    KEY_ALL_ACCESS = winreg.KEY_ALL_ACCESS
    DEBUG = False
    
    OPEN_KEY = winreg.CreateKeyEx(
        HKEYCU,     # *HKEY_CURRENT_USER...
        KEY_NAME,   # *...\\Console
        0,          # * reserved = 0
        KEY_ALL_ACCESS
        )
        
    # * Index 1: An integer giving the number of values this key has.
    # *          
    # * https://docs.python.org/3/library/winreg.html#winreg.QueryInfoKey
    values_length = winreg.QueryInfoKey(OPEN_KEY)[1]
    values = []
    
    for i in range(0, values_length):
        # * Index 0: A string that identifies the value name
        # * Index 1: An object that holds the value data, and whose 
        # *          type depends on the underlying registry type
        # * Index 2: An integer that identifies the type of the value
        # *          data (see table in docs for SetValueEx())
        # *
        # * https://docs.python.org/3/library/winreg.html#winreg.EnumValue
    
        value = winreg.EnumValue(OPEN_KEY, i)

        # * Check if the registry value is equal to
        # * >>> ('VirtualTerminalLevel', 1, 4)
        if value[0] == VALUE_NAME:
            if value[1] == DWORD_VALUE:
                if value[2] == winreg.REG_DWORD:
                    if DEBUG:
                        print(
                            "[!] Query succeed\n"
                            f"[+] Key queried {FULL_KEY}: {DWORD_VALUE}"
                            )

                    
                    return True
    
    winreg.SetValueEx(
        OPEN_KEY,
        VALUE_NAME,
        0,
        winreg.REG_DWORD,
        DWORD_VALUE
        )

    values_length = winreg.QueryInfoKey(OPEN_KEY)[1]
    for i in range(0, values_length):
        value = winreg.EnumValue(OPEN_KEY, i)

        if value[0] == VALUE_NAME:
            if value[1] == DWORD_VALUE:
                if value[2] == winreg.REG_DWORD:
                    if DEBUG:
                        print(
                            "[!] Query succeed\n"
                            f"[+] Key queried {FULL_KEY}: {DWORD_VALUE}"
                            )
                    
                    return True
    print("[!] Can't write to the registry, try"
          " running the script as administrator")
    return False

TERMVIRT_SUPPORT = _check_termvirt()

if TERMVIRT_SUPPORT == True:
    G = '\033[92m'
    R = '\033[31m'
    Y = '\033[33m'
    C = '\033[94m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    SMSO = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[6m'
    INVISIBLE = '\033[7m'
    DEF = '\033[0m'
else:
    G = ''
    R = ''
    Y = ''
    C = ''
    BOLD = ''
    DIM = ''
    SMSO = ''
    UNDERLINE = ''
    BLINK = ''
    REVERSE = ''
    INVISIBLE = ''
        
        
COLORS = {
    'none': '',
    'default': DEF,
    'green': G,
    'red': R,
    'yellow': Y,
    'cyan': C
    }
    
EFFECTS = {
    'none': '',
    'default': DEF,
    'bold': BOLD,
    'dim': DIM,
    'smso': SMSO,
    'underline': UNDERLINE,
    'blink': BLINK,
    'reverse': REVERSE,
    'invisible': INVISIBLE
    }

