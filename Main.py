import wx
import sys
import win32api

import win32clipboard

import win32gui
import win32ui
import win32con
import win32api

import ctypes
from ctypes import windll, byref, c_short, c_char, c_uint8, c_int32, c_int, c_uint, c_uint32, c_long, Structure, CFUNCTYPE, POINTER
from ctypes.wintypes import WORD, DWORD, BOOL, HHOOK, MSG, LPWSTR, WCHAR, WPARAM, LPARAM, LONG, ULONG
import atexit

class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.SetSize((500, 400))

    def OnExit(self, event):
        self.Close(True)


#if __name__ == "__main__":
    #Create the Main frame
    #app = wx.App(False)
    #frame = MainFrame(None, title="Screenshotshare")
    #frame.Show()
    #app.MainLoop()

# Let's see if I can get hooks working through my own efforts and not libraries.
# Time to clutch tightly to the msdn... and pray It'll all work.
# https://msdn.microsoft.com/en-us/library/windows/desktop/ms632589(v=vs.85).aspx
user32 = ctypes.WinDLL('user32', use_last_error=True)

ULONG_PTR = POINTER(ULONG)
NULL = c_int(0)
WH_KEYBOARD_LL = c_int(13)  # WH_KEYBOARD_LL == 13

# Invoke Windows API SetWindowsHookEx, CallNextHookEx, UnhookWindowsHookEx, and GetModuleHandle.

# HHOOK WINAPI SetWindowsHookEx(_In_ int idHook, _In_ HOOKPROC lpfn, _In_ HINSTANCE hMod,_In_ DWORD dwThreadId);
# https://msdn.microsoft.com/en-us/library/ms644990(VS.85).aspx
SetWindowsHookEx = user32.SetWindowsHookExA  # # ExA = ANSI -- ExW = Unicode
SetWindowsHookEx.restype = HHOOK  # restype sets the return type, by default it assume C int

# LRESULT WINAPI CallNextHookEx(_In_opt_ HHOOK  hhk, _In_ int    nCode, _In_ PARAM wParam, _In_ LPARAM lParam);
# https://msdn.microsoft.com/en-us/library/ms644974(v=vs.85).aspx
CallNextHookEx = user32.CallNextHookEx
CallNextHookEx.restype = c_int  # Keyboard events seem to return an int

UnhookWindowsHookEx = user32.UnhookWindowsHookEx

#LRESULT CALLBACK LowLevelKeyboardProc(
#  _In_ int    nCode,
#  _In_ WPARAM wParam,
#  _In_ LPARAM lParam -- Pointer to KBDLLHOOKSTRUCT
#);
def low_level_handler(nCode, wParam, lParam):
    print('n: ' + str(nCode))
    print('w: ' + str(wParam))
    print('l: ' + str(lParam) + ' ' + str(lParam.contents.vk_code))
    # TODO: Read the docs and make this CallNextHook proper
    return CallNextHookEx(NULL, nCode, wParam, lParam)


class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [("vk_code", DWORD),
                ("scan_code", DWORD),
                ("flags", DWORD),
                ("time", c_int),
                ("dwExtraInfo", ULONG_PTR)]


LowLevelKeyboardProc = CFUNCTYPE(c_int, c_int, LPARAM, POINTER(KBDLLHOOKSTRUCT))
keyboardcallback = LowLevelKeyboardProc(low_level_handler)

# HHOOK WINAPI SetWindowsHookEx(_In_ int idHook, _In_ HOOKPROC lpfn, _In_ HINSTANCE hMod,_In_ DWORD dwThreadId)
keyboardhook = SetWindowsHookEx(WH_KEYBOARD_LL, keyboardcallback, NULL, NULL)

# Unregister the hook at exit
atexit.register(UnhookWindowsHookEx, keyboardcallback)

while True:
    msg = windll.user32.GetMessageW(None, 0, 0, 0)
    windll.user32.TranslateMessage(byref(msg))
    windll.user32.DispatchMessageW(byref(msg))
