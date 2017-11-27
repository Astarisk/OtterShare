import wx
import WinKeyboard
import Config
import Screenshot
import ImageUpload
import threading
import os
from KeyboardEvent import KEY_DOWN, KEY_UP, KeyboardEvent as KeyboardEvent
from TaskBarIcon import TaskBarIcon

# TODO: Make sure only a windows OS loads this
class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title="Otter Share")
        panel = wx.Panel(self)

        self.tbIcon = TaskBarIcon(self)

        self.Bind(wx.EVT_ICONIZE, self.OnMinimize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.Show()
        # Add some events to the keyboard
        #WinKeyboard.add_handler(print_event)
        WinKeyboard.add_handler(screenshot_handler)
        # Start listening on keystrokes
        self.worker = None

        if not self.worker:
            self.worker = threading.Thread(target=WinKeyboard.listener())
            self.worker.start()

    def OnClose(self, event):
        WinKeyboard.stop_pumping(threading.get_ident())
        self.tbIcon.RemoveIcon()
        self.tbIcon.Destroy()
        self.Destroy()

    def OnMinimize(self, event):
        if self.IsIconized():
            self.Hide()


def print_event(event):
    print(event)


def screenshot_handler(event):
    # TODO: Work on the Keyboard so it's more flexible in regards to key pressing.
    if event.event_type == KEY_UP and event.name in Config.get_save_hotkey():
        WinKeyboard.lock = False

    if set(Config.get_save_hotkey()) == set(WinKeyboard.keys_down) and not WinKeyboard.lock:
        WinKeyboard.lock = True
        img = Screenshot.take_picture()

        if Config.get_save_img:
            Screenshot.save_picture(img, Config.get_save_location())
        if Config.get_upload_img:
            ImageUpload.upload_img(img, Config.get_client_id(), Config.get_save_location())


def main():
    # Add some events to the keyboard
    #Create the Main frame
    if os.name != 'nt':
        print('This application is not supported on: ' + os.name)
        return
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
