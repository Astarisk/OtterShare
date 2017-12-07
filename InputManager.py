import ctypes
from ctypes import c_int, CFUNCTYPE, POINTER
from ctypes.wintypes import DWORD, BOOL, HHOOK, MSG, LPARAM, ULONG, POINT, UINT, HWND
import atexit
import win32con
import win32gui
import win32api

# Let's see if I can get hooks working through my own efforts and not libraries.
# Time to clutch tightly to the msdn... and pray It'll all work.
# https://msdn.microsoft.com/en-us/library/windows/desktop/ms632589(v=vs.85).aspx
user32 = ctypes.WinDLL('user32', use_last_error=True)

ULONG_PTR = POINTER(ULONG)
NULL = c_int(0)
LPMSG = POINTER(MSG)
# Invoke Windows API SetWindowsHookEx, CallNextHookEx, UnhookWindowsHookEx, and GetModuleHandle.

# HHOOK WINAPI SetWindowsHookEx(_In_ int idHook, _In_ HOOKPROC lpfn, _In_ HINSTANCE hMod,_In_ DWORD dwThreadId);
# https://msdn.microsoft.com/en-us/library/ms644990(VS.85).aspx
SetWindowsHookEx = user32.SetWindowsHookExA  # # ExA = ANSI -- ExW = Unicode
SetWindowsHookEx.restype = HHOOK  # restype sets the return type, by default it assume C int

# LRESULT WINAPI CallNextHookEx(_In_opt_ HHOOK  hhk, _In_ int    nCode, _In_ PARAM wParam, _In_ LPARAM lParam);
# https://msdn.microsoft.com/en-us/library/ms644974(v=vs.85).aspx
CallNextHookEx = user32.CallNextHookEx
CallNextHookEx.restype = c_int  # Keyboard events seem to return an int

# BOOL WINAPI UnhookWindowsHookEx(_In_ HHOOK hhk);
# https://msdn.microsoft.com/en-us/library/ms644993(v=vs.85).aspx
UnhookWindowsHookEx = user32.UnhookWindowsHookEx
UnhookWindowsHookEx.argtypes = [HHOOK]
UnhookWindowsHookEx.restype = BOOL


# Retrieves a message from the calling thread's message queue. The function dispatches incoming sent messages
# until a posted message is available for retrieval.
# https://msdn.microsoft.com/en-us/library/ms644936(v=vs.85).aspx
GetMessage = user32.GetMessageW
GetMessage.argtypes = [LPMSG, c_int, c_int, c_int]
GetMessage.restype = BOOL

PeekMessage = user32.PeekMessageW
PeekMessage.argtypes = [LPMSG, c_int, c_int, c_int, c_int]
PeekMessage.restype = BOOL

inputs = []
low_level_handlers = []
handlers = []
callbacks = []
hooks = []


def listener():

    def process_event(event):
        for h in handlers:
            h(event)

    for i in inputs:
        handler = i.generate_handler()
        handlers.append(i.generate_handler())
        callback = i.generate_callback(handler)
        callbacks.append(callback)
        hook = i.generate_hook(callback)
        hooks.append(hook)

    # Unregister the hook at exit
    def unhook_register():
        print('unhooked')
        for i in inputs:
            i.unhook()

    atexit.register(unhook_register)

    # Retrieves a message from the calling thread's message queue. The function dispatches incoming sent messages until
    # a posted message is available for retrieval.
    print("Begin pumping..")
    win32gui.PumpMessages()


def add_input(inp):
    inputs.append(inp)


def stop_pumping(thread_id):
    # Posts a Quit message to the message queue
    win32api.PostThreadMessage(thread_id, win32con.WM_QUIT, 0, 0)
