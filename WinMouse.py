import Input
from Input import Input as InputBase
from MouseEvent import MouseEvent as MouseEvent

# https://msdn.microsoft.com/en-us/library/windows/desktop/ms644968(v=vs.85).aspx
class tagMOUSEHOOKSTRUCT(Input.ctypes.Structure):
    _fields_ = [("pt", Input.POINT),
                ("hwnd", Input.HWND),
                ("wHitTestCode", Input.UINT),
                ("dwExtraInfo", Input.ULONG_PTR)]

# From the MSDN, the hook id for global mouse is 14
WH_MOUSE_LL = Input.c_int(14)


class WinMouse(InputBase):
    def generate_handler(self):
        def low_level_handler(nCode, wParam, lParam):
            event = MouseEvent(wParam)
            print(event)
            return Input.CallNextHookEx(Input.NULL, nCode, wParam, lParam)
        return low_level_handler

    def generate_callback(self, handler):
        CMPFUNC = Input.CFUNCTYPE(Input.c_int, Input.c_int, Input.LPARAM, Input.POINTER(tagMOUSEHOOKSTRUCT))
        callback = CMPFUNC(handler)
        return callback

    def generate_hook(self, callback):
        hook = Input.SetWindowsHookEx(WH_MOUSE_LL, callback, Input.NULL, Input.NULL)
        self.hook = hook
        return hook