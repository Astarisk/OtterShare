import wx
import sys
import WinKeyboard
import Config
import Screenshot
import ImageUpload
from KeyboardEvent import KEY_DOWN, KEY_UP, KeyboardEvent as KeyboardEvent

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

def print_event(event):
    print(event)


def screenshot_handler(event):
    # TODO: Work on the Keyboard so it's more flexible in regards to key pressing.
    if event.event_type == KEY_UP and event.name in Config.save_hotkey:
        WinKeyboard.lock = False

    if set(Config.save_hotkey) == set(WinKeyboard.keys_down) and WinKeyboard.lock == False:
        WinKeyboard.lock = True

        img = Screenshot.take_picture()

        if Config.save_img:
            Screenshot.save_picture(img, Config.save_location)
        #if Config.upload_img:
        #    ImageUpload.upload_img(img, Config.client_id)


def quit_program(event):
    if event.name == 'z':
        sys.exit()


#WinKeyboard.add_handler(print_event)
WinKeyboard.add_handler(screenshot_handler)
WinKeyboard.add_handler(quit_program)

WinKeyboard.listener()
