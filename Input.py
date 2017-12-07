import ctypes
from ctypes import c_int, CFUNCTYPE, POINTER
from ctypes.wintypes import DWORD, BOOL, HHOOK, MSG, LPARAM, ULONG, POINT, UINT, HWND
from abc import ABC, abstractmethod

# Defining more variables from C
ULONG_PTR = POINTER(ULONG)
NULL = c_int(0)
LPMSG = POINTER(MSG)

# LRESULT WINAPI CallNextHookEx(_In_opt_ HHOOK  hhk, _In_ int    nCode, _In_ PARAM wParam, _In_ LPARAM lParam);
# https://msdn.microsoft.com/en-us/library/ms644974(v=vs.85).aspx
# CallNextHookEx = user32.CallNextHookEx
# CallNextHookEx.restype = c_int  # Keyboard events seem to return an int

# https://msdn.microsoft.com/en-us/library/windows/desktop/ms632589(v=vs.85).aspx
user32 = ctypes.WinDLL('user32', use_last_error=True)

# LRESULT WINAPI CallNextHookEx(_In_opt_ HHOOK  hhk, _In_ int    nCode, _In_ PARAM wParam, _In_ LPARAM lParam);
# https://msdn.microsoft.com/en-us/library/ms644974(v=vs.85).aspx
CallNextHookEx = user32.CallNextHookEx
CallNextHookEx.restype = c_int  # Keyboard events seem to return an int

# HHOOK WINAPI SetWindowsHookEx(_In_ int idHook, _In_ HOOKPROC lpfn, _In_ HINSTANCE hMod,_In_ DWORD dwThreadId);
# https://msdn.microsoft.com/en-us/library/ms644990(VS.85).aspx
SetWindowsHookEx = user32.SetWindowsHookExA  # # ExA = ANSI -- ExW = Unicode
SetWindowsHookEx.restype = HHOOK  # restype sets the return type, by default it assume C int

# BOOL WINAPI UnhookWindowsHookEx(_In_ HHOOK hhk);
# https://msdn.microsoft.com/en-us/library/ms644993(v=vs.85).aspx
UnhookWindowsHookEx = user32.UnhookWindowsHookEx
UnhookWindowsHookEx.argtypes = [HHOOK]
UnhookWindowsHookEx.restype = BOOL


class Input(ABC):

    def __init__(self):
        self.hook = None
        self.handler = None
        self.callback = None

    @abstractmethod
    def generate_handler(self):
        def low_level_handler(nCode, wParam, lParam):
            pass

    @abstractmethod
    def generate_callback(self, handler):
        pass

    @abstractmethod
    def generate_hook(self, callback):
        pass

    def unhook(self):
        UnhookWindowsHookEx(self.hook)

