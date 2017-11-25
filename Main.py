import wx
import sys
import ctypes
from ctypes import windll, byref, c_short, c_char, c_uint8, c_int32, c_int, c_uint, c_uint32, c_long, Structure, CFUNCTYPE, POINTER
from ctypes.wintypes import WORD, DWORD, BOOL, HHOOK, MSG, LPWSTR, WCHAR, WPARAM, LPARAM, LONG, ULONG
import Screenshot
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
LPMSG = POINTER(MSG)


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
    WM_KEYDOWN: 'Key Down',
    WM_KEYUP: 'Key Up',
    WK_SYSKEYDOWN: 'Key Down',
    WK_SYSKEYUP: 'Key up'
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


def listener():
    def low_level_handler(nCode, wParam, lParam):
        if lParam.contents.vk_code in virtual_keys:
            print('n: ' + str(nCode))
            print('w: ' + str(key_identifier[wParam]))
            print('l: ' + str(lParam) + ' ' + virtual_keys[lParam.contents.vk_code])
            if virtual_keys[lParam.contents.vk_code] == 'z':
                sys.exit()
            if virtual_keys[lParam.contents.vk_code] == 'p':
                Screenshot.save_picture()

        print("Call next hook")
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
        print("Did it unhook?")
        print(UnhookWindowsHookEx(keyboardhook))

    # atexit.register(UnhookWindowsHookEx, keyboardhook)
    atexit.register(unhook_register)

    # Retrieves a message from the calling thread's message queue. The function dispatches incoming sent messages until
    # a posted message is available for retrieval
    GetMessage(LPMSG(), NULL, NULL, NULL)


listener()






