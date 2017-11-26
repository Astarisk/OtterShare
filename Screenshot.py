import win32gui
import win32ui
import win32con
import win32api

from datetime import datetime
from PIL import Image


'''
   https://msdn.microsoft.com/en-us/library/windows/desktop/dd183402(v=vs.85).aspx
   To store an image temporarily, your application must call CreateCompatibleDC to create a DC that is compatible with
   the current window DC. After you create a compatible DC, you create a bitmap with the appropriate dimensions by 
   calling the CreateCompatibleBitmap function and then select it into this device context by calling the
   SelectObject function.
   '''

# Grab the width, Height, and Top Left of the screen -- This is for ALL monitors
# https://msdn.microsoft.com/en-us/library/windows/desktop/ms724385(v=vs.85).aspx
def take_picture():
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    # Grabs the desktop window handle
    desktophandle = win32gui.GetDesktopWindow()
    windowrect = win32gui.GetClientRect(desktophandle)

    # Create device contexts:
    # A device context is a structure that defines a set of graphic objects
    # and their associated attributes, as well as the graphic modes that affect output.
    desktopcontext = win32gui.GetDC(desktophandle)
    imgdc = win32ui.CreateDCFromHandle(desktopcontext)  # This is a PyCDC object, PyCDeviceContext

    # Create memory device context, stores the bitmap until save
    memdc = imgdc.CreateCompatibleDC()

    # Create bitmap object
    screen = win32ui.CreateBitmap()
    screen.CreateCompatibleBitmap(imgdc, width, height)

    # Points the memdc to the newly created bitmap
    memdc.SelectObject(screen)

    # Copy from screen to new bitmap
    memdc.BitBlt((0, 0), (width, height), imgdc, (0, 0), win32con.SRCCOPY)

    # Turn img into a png
    info = screen.GetInfo()
    size = (info['bmWidth'], info['bmHeight'])
    buf = screen.GetBitmapBits(True)
    img = Image.frombuffer('RGB', size, buf, 'raw', 'BGRX', 0, 1)

    # free objects
    memdc.DeleteDC()
    win32gui.DeleteObject(screen.GetHandle())
    return img


def save_picture(img, savedir):
    img.save(savedir + generate_filename() + '.png', 'png')


def generate_filename():
    # TODO: Maybe add in more options such as tags? Saving in folders based on tags? etc
    # Generate the file name based on date and time
    date = str(datetime.now())
    filename = date[:10] + ' at ' + date[11:19].replace(':', '.')
    return filename

