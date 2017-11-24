import wx
import sys
import win32api

import win32clipboard

import win32gui
import win32ui
import win32con
import win32api


class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.SetSize((500, 400))

    def OnExit(self, event):
        self.Close(True)


if __name__ == "__main__":
    # Create the Main frame
    #app = wx.App(False)
    #frame = MainFrame(None, title="Screenshotshare")
    #frame.Show()
    #app.MainLoop()

    win32clipboard.OpenClipboard()
    d = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)

    print(d)

    '''
    https://msdn.microsoft.com/en-us/library/windows/desktop/dd183402(v=vs.85).aspx
    To store an image temporarily, your application must call CreateCompatibleDC to create a DC that is compatible with
    the current window DC. After you create a compatible DC, you create a bitmap with the appropriate dimensions by 
    calling the CreateCompatibleBitmap function and then select it into this device context by calling the
    SelectObject function.
    '''

    # Grab the width, Height, and Top Left of the screen -- This is for ALL monitors
    # https://msdn.microsoft.com/en-us/library/windows/desktop/ms724385(v=vs.85).aspx

    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    savedir = 'c:\\users\\keith\\desktop\\screenshot.bmp'


    # Grabs the desktop window handle
    desktophandle = win32gui.GetDesktopWindow()
    windowrect = win32gui.GetClientRect(desktophandle)

    # Create device contexts:
    # A device context is a structure that defines a set of graphic objects
    # and their associated attributes, as well as the graphic modes that affect output.
    desktopcontext = win32gui.GetDC(desktophandle)
    imgdc = win32ui.CreateDCFromHandle(desktopcontext)  # This is a PyCDC object, PyCDeviceContext
    print(imgdc)
    # Create memory device context, stores the bitmap until save
    memdc = imgdc.CreateCompatibleDC()
    print(memdc)
    # Create bitmap object
    screen = win32ui.CreateBitmap()
    screen.CreateCompatibleBitmap(imgdc, width, height)

    # Points the memdc to the newly created bitmap
    memdc.SelectObject(screen)

    # Copy from screen to new bitmap
    # BitBlt(destPos, size, dc, srcPos, rop)
    memdc.BitBlt((0, 0), (width, height), imgdc, (0, 0), win32con.SRCCOPY)
    # save the bitmap to a file
    screen.SaveBitmapFile(memdc, savedir)

    # free objects
    memdc.DeleteDC()
    win32gui.DeleteObject(screen.GetHandle())

