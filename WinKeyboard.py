import Input
from Input import Input as InputBase
from KeyboardEvent import KEY_DOWN, KEY_UP, KeyboardEvent as KeyboardEvent


# https://msdn.microsoft.com/en-us/library/ms644967(v=vs.85).aspx
class KBDLLHOOKSTRUCT(Input.ctypes.Structure):
    _fields_ = [("vk_code", Input.DWORD),
                ("scan_code", Input.DWORD),
                ("flags", Input.DWORD),
                ("time", Input.c_int),
                ("dwExtraInfo", Input.ULONG_PTR)]


WH_KEYBOARD_LL = Input.c_int(13)

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
    0x41: 'a',    0x42: 'b',    0x43: 'c',    0x44: 'd',
    0x45: 'e',    0x46: 'f',    0x47: 'g',    0x48: 'h',
    0x49: 'i',    0x4A: 'j',    0x4B: 'k',    0x4C: 'l',
    0x4D: 'm',    0x4E: 'n',    0x4F: 'o',    0x50: 'p',
    0x51: 'q',    0x52: 'r',    0x53: 's',    0x54: 't',
    0x55: 'u',    0x56: 'v',    0x57: 'w',    0x58: 'x',
    0x59: 'y',    0x5A: 'z',    0xA0: 'shift',    0xA2: 'ctrl',
    0xA4: 'alt'
}


class WinKeyboard(InputBase):
    def generate_handler(self):
        def low_level_handler(nCode, wParam, lParam):
            if lParam.contents.vk_code in virtual_keys:
                event = KeyboardEvent(key_identifier[wParam], virtual_keys[lParam.contents.vk_code])
                print(event)
            return Input.CallNextHookEx(Input.NULL, nCode, wParam, lParam)
        return low_level_handler

    def generate_callback(self, handler):
        CMPFUNC = Input.CFUNCTYPE(Input.c_int, Input.c_int, Input.LPARAM, Input.POINTER(KBDLLHOOKSTRUCT))
        callback = CMPFUNC(handler)
        return callback

    def generate_hook(self, callback):
        hook = Input.SetWindowsHookEx(WH_KEYBOARD_LL, callback, Input.NULL, Input.NULL)
        self.hook = hook
        return hook
