import wx
import wx.adv
import Config


class TaskBarIcon(wx.adv.TaskBarIcon):

    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame

        img = wx.Image("res/otter.png", wx.BITMAP_TYPE_ANY)
        bmp = wx.Bitmap(img)

        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(bmp)

        self.SetIcon(self.icon, "Restore")
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.OnTaskBarRightClick)

    def OnTaskBarRightClick(self, event):
        menu = self.CreatePopupMenu()
        self.PopupMenu(menu)
        menu.Destroy()

    def onOpen(self, event):
        self.frame.Restore()

    def onClose(self, event):
        # TODO: This close won't work, It'll hang then crash.
        self.frame.OnClose(event)
        self.Destroy()

    def onReload(self, event):
        Config.load_config()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        item = menu.Append(wx.ID_ANY, "Open Program")
        self.Bind(wx.EVT_MENU, self.onOpen, item)
        item = menu.Append(wx.ID_ANY, "Reload Config")
        self.Bind(wx.EVT_MENU, self.onReload, item)
        #item = menu.Append(wx.ID_ANY, "Close Program")
        #self.Bind(wx.EVT_MENU, self.onClose, item)
        return menu
