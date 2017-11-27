import ctypes
from ctypes import c_int, CFUNCTYPE, POINTER
# windll, byref, c_short, c_char ,c_uint, c_uint8, c_int32, c_long, Structure,
from ctypes.wintypes import DWORD, BOOL, HHOOK, MSG, LPARAM, ULONG
#  WORD,  LPWSTR, WCHAR, WPARAM,  LONG,
import atexit
import sys
from KeyboardEvent import KEY_DOWN, KEY_UP, KeyboardEvent as KeyboardEvent

# Let's see if I can get hooks working through my own efforts and not libraries.
# Time to clutch tightly to the msdn... and pray It'll all work.
# https://msdn.microsoft.com/en-us/library/windows/desktop/ms632589(v=vs.85).aspx
user32 = ctypes.WinDLL('user32', use_last_error=True)


ULONG_PTR = POINTER(ULONG)
NULL = c_int(0)
LPMSG = POINTER(MSG)

# https://msdn.microsoft.com/en-us/library/ms644967(v=vs.85).aspx
class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [("vk_code", DWORD),
                ("scan_code", DWORD),
                ("flags", DWORD),
                ("time", c_int),
                ("dwExtraInfo", ULONG_PTR)]


WH_KEYBOARD_LL = c_int(13)  # WH_KEYBOARD_LL == 13

WM_KEYDOWN = 0X0100
WM_KEYUP = 0X0101
WK_SYSKEYDOWN = 0X0104
WK_SYSKEYUP = 0X0105

key_identifier = {
    WM_KEYDOWN: KEY_DOWN,
    WM_KEYUP: KEY_UP,
    WK_SYSKEYDOWN: KEY_DOWN,
    WK_SYSKEYUP: KEY_UP
}


virtual_keys = {
    0x41: 'a',
    0x42: 'b',
    0x43: 'c',
    0x44: 'd',
    0x45: 'e',
    0x46: 'f',
    0x47: 'g',
    0x48: 'h',
    0x49: 'i',
    0x4A: 'j',
    0x4B: 'k',
    0x4C: 'l',
    0x4D: 'm',
    0x4E: 'n',
    0x4F: 'o',
    0x50: 'p',
    0x51: 'q',
    0x52: 'r',
    0x53: 's',
    0x54: 't',
    0x55: 'u',
    0x56: 'v',
    0x57: 'w',
    0x58: 'x',
    0x59: 'y',
    0x5A: 'z',
    0xA0: 'shift',
    0xA2: 'ctrl',
    0xA4: 'alt'
}
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

handlers = []

#modifier_keys = {
#    0x010: 'Shift',
#    0x011: 'Ctrl',
#    0x012: 'Alt'
#}

modifier_keys = {
    'shift': False,
    'ctrl': False,
    'alt': True
}

SHIFT_DOWN = False
CTRL_DOWN = False
ALT_DOWN = False

lock = False
keys_down = set([])


def listener():

    def process_event(event):
        for h in handlers:
            h(event)

    def low_level_handler(nCode, wParam, lParam):
        if lParam.contents.vk_code in virtual_keys:
            event = KeyboardEvent(key_identifier[wParam], virtual_keys[lParam.contents.vk_code])

            process_event(event)
        # TODO: Read the docs and make this CallNextHook proper
        return CallNextHookEx(NULL, nCode, wParam, lParam)

    # Low level handler signature
    # LRESULT CALLBACK LowLevelKeyboardProc(
    #  _In_ int    nCode, -- If nCode is less than zero, the hook procedure must pass the message to the CallNextHookEx
    #  _In_ WPARAM wParam,-- The identifier of the keyboard message.
    #  This parameter can be one of the following messages: WM_KEYDOWN, WM_KEYUP, WM_SYSKEYDOWN, or WM_SYSKEYUP.

    #  _In_ LPARAM lParam -- Pointer to KBDLLHOOKSTRUCT
    # );
    CMPFUNC = CFUNCTYPE(c_int, c_int, LPARAM, POINTER(KBDLLHOOKSTRUCT))
    # Converts it to a C pointer
    keyboardcallback = CMPFUNC(low_level_handler)

    # HHOOK WINAPI SetWindowsHookEx(_In_ int idHook, _In_ HOOKPROC lpfn, _In_ HINSTANCE hMod,_In_ DWORD dwThreadId)
    # https://msdn.microsoft.com/en-us/library/ms644990(v=vs.85).aspx
    keyboardhook = SetWindowsHookEx(WH_KEYBOARD_LL, keyboardcallback, NULL, NULL)

    # Unregister the hook at exit
    def unhook_register():
        UnhookWindowsHookEx(keyboardhook)

    # atexit.register(UnhookWindowsHookEx, keyboardhook)
    atexit.register(unhook_register)

    # Retrieves a message from the calling thread's message queue. The function dispatches incoming sent messages until
    # a posted message is available for retrieval
    GetMessage(LPMSG(), NULL, NULL, NULL)


def add_to_set(event):
    if event.event_type == KEY_DOWN:
        print("Added:" + str(event.event_type) + " " + str(keys_down))
        keys_down.add(event.name)


def remove_from_set(event):
    if event.event_type == KEY_UP:
        print("Removed:" + str(event.event_type) + " " + str(keys_down))
        keys_down.remove(event.name)


def add_handler(handler):
    handlers.append(handler)



add_handler(add_to_set)
add_handler(remove_from_set)





