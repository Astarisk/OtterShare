import wx
import sys
import WinKeyboard
import Config
import Screenshot
import ImageUpload

# TODO: Make sure only a windows OS loads this
class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.SetSize((500, 400))

    def OnExit(self, event):
        self.Close(True)


#if __name__ == "__main__":
    #Create the Main frame
    #app = wx.App(False)
    #frame = MainFrame(None, title="OtterShare")
    #frame.Show()
    #app.MainLoop()

# Start listening on keystrokes

def print_event(e):
    print(e)


def screenshot_handler(e):
    # TODO: Set this on key up and allow multiple key press combinations
    if e.name == Config.save_hotkey:
        img = Screenshot.take_picture()

        if Config.save_img:
            Screenshot.save_picture(img, Config.save_location)
        if Config.upload_img:
            ImageUpload.upload_img(img, Config.client_id)


def quit_program(e):
    if e.name == 'z':
        sys.exit()


WinKeyboard.add_handler(print_event)
WinKeyboard.add_handler(screenshot_handler)
WinKeyboard.add_handler(quit_program)

WinKeyboard.listener()
