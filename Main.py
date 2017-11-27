import wx
import sys
import WinKeyboard
import Config
import Screenshot
import ImageUpload
from KeyboardEvent import KEY_DOWN, KEY_UP, KeyboardEvent as KeyboardEvent
from TaskBarIcon import TaskBarIcon

# TODO: Make sure only a windows OS loads this
class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title="Otter Share")



def print_event(event):
    print(event)


def screenshot_handler(event):
    # TODO: Work on the Keyboard so it's more flexible in regards to key pressing.
    if event.event_type == KEY_UP and event.name in Config.save_hotkey:
        WinKeyboard.lock = False

    if set(Config.save_hotkey) == set(WinKeyboard.keys_down) and not WinKeyboard.lock:
        WinKeyboard.lock = True
        print("picture taken")
        img = Screenshot.take_picture()

        if Config.save_img:
            Screenshot.save_picture(img, Config.save_path_location())
        #if Config.upload_img:
        #    ImageUpload.upload_img(img, Config.client_id)


def quit_program(event):
    if event.name == 'z':
        sys.exit()


def main():
    # Add some events to the keyboard
    #Create the Main frame
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    # Add some events to the keyboard
    WinKeyboard.add_handler(print_event)
    WinKeyboard.add_handler(screenshot_handler)
    WinKeyboard.add_handler(quit_program)
    # Start listening on keystrokes
    print("Listening..")
    WinKeyboard.listener()
    #main()
