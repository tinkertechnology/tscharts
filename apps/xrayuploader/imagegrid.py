import wx
from pubsub import pub

class ImageGrid(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
       
        #self.grid = wx.GridSizer(5, 4, 5, 5)
        self.grid = wx.GridSizer(5, 5, 5, 5)
        self.parent = parent 
        '''
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.SetSizer(sizer)
        '''
        self.SetMinSize(wx.Size(300, 300))
        self.SetSizer(self.grid)
        self.Layout()
        self.Show()
        pub.subscribe(self.on_clear_message, 'clearxrays')      

    def add(self, path):
        photoMaxSize = 60
        img = wx.Image(photoMaxSize, photoMaxSize)
        imageCtrl = wx.StaticBitmap(self, wx.ID_ANY,
                                         wx.Bitmap(img))
        img = wx.Image(path, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = photoMaxSize
            NewH = photoMaxSize * H / W
        else:
            NewH = photoMaxSize
            NewW = photoMaxSize * W / H
        img = img.Scale(NewW,NewH)
        imageCtrl.SetBitmap(wx.Bitmap(img))
        self.grid.Add(imageCtrl)
        self.grid.ShowItems(True)
        pub.sendMessage("refresh")
        #self.parent.Refresh()

    def on_clear_message(self):
        self.grid.ShowItems(False)
        self.clear();
        self.Layout()
        pub.sendMessage("refresh")
 
    def clear(self):
        print("clear")
        try:
            self.grid.Clear()
        except:
            pass
