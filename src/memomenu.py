import wx

class MemoMenu():
    def __init__(self, parent):
        self.parent = parent
        self._addMenubar()

    def _addMenubar(self):
        menubar = wx.MenuBar()

        ##
        fileMenu = wx.Menu()

        saveFilteredItemsId = wx.NewId()
        saveFilteredItems = fileMenu.Append(saveFilteredItemsId, 'Save filtered items', 'Save filtered items')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSaveFilteredItems, saveFilteredItems)

        fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit App')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnQuit, fileItem)
        menubar.Append(fileMenu, '&File')

        ##
        viewMenu = wx.Menu()

        bgBlackColorItemsId = wx.NewId()
        bgBlackColorItems = viewMenu.Append(bgBlackColorItemsId, 'Set Black', 'Set backgourd as Black')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSetBlackColorBg, bgBlackColorItems)

        bgBlueColorItemsId = wx.NewId()
        bgBlueColorItems = viewMenu.Append(bgBlueColorItemsId, 'Set Blue', 'Set backgourd as Blue')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSetBlueColorBg, bgBlueColorItems)

        bgWhiteColorItemsId = wx.NewId()
        bgWhiteColorItems = viewMenu.Append(bgWhiteColorItemsId, 'Set White', 'Set backgourd as White')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSetWhiteColorBg, bgWhiteColorItems)

        bgYellowColorItemsId = wx.NewId()
        bgYellowColorItems = viewMenu.Append(bgYellowColorItemsId, 'Set Yellow', 'Set backgourd as Yellow')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSetYellowColorBg, bgYellowColorItems)

        menubar.Append(viewMenu, '&View')

        ##
        helpMenu = wx.Menu()

        aboutItemId = wx.NewId()
        aboutItem = helpMenu.Append(aboutItemId, 'About', 'About')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnAbout, aboutItem)
        menubar.Append(helpMenu, '&Help')

        self.parent.SetMenuBar(menubar)
