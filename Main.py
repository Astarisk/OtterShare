import wx
import sys
import WinKeyboard

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

# Start listening on keystrokes
WinKeyboard.listener()
