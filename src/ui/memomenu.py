import wx

class MemoMenu:
    def __init__(self, parent, _config):
        self.parent = parent
        self.config = _config
        self._addMenubar()

    def _addMenubar(self):
        menubar = wx.MenuBar()

        self._add_file_menu(menubar)
        self._add_edit_menu(menubar)
        self._add_find_menu(menubar)
        self._add_view_menu(menubar)
        self._add_help_menu(menubar)

        self.parent.SetMenuBar(menubar)

    def _add_file_menu(self, menubar):
        file_menu = wx.Menu()

        set_max_view_count_id = wx.NewId()
        set_max_view_count = file_menu.Append(set_max_view_count_id, 'Set max view &count', 'Set max view count')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_set_max_list, set_max_view_count)

        save_filtered_items_id = wx.NewId()
        save_filtered_items = file_menu.Append(save_filtered_items_id, '&Save filtered items', 'Save filtered items')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSaveFilteredItems, save_filtered_items)

        file_item = file_menu.Append(wx.ID_EXIT, '&Quit', 'Quit App')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnQuit, file_item)
        menubar.Append(file_menu, '&File')

    def _add_edit_menu(self, menubar):
        edit_menu = wx.Menu()

        clone_memo_id = wx.NewId()
        clone_memo = edit_menu.Append(clone_memo_id, '&Clone meno', 'Clone memo')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_clone_memo, clone_memo)

        menubar.Append(edit_menu, '&Edit')

    def _add_find_menu(self, menubar):
        find_menu = wx.Menu()

        set_config_item_id = wx.NewId()
        set_config_item = find_menu.Append(set_config_item_id, 'Set Filter Items', '')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_set_config_menu, set_config_item)

        ctrl_1_item_id = wx.NewId()
        self.ctrl_1_item = find_menu.Append(ctrl_1_item_id, self.__get_menu_text('ctrl_1'), '')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_ctrl_1, self.ctrl_1_item)

        ctrl_2_item_id = wx.NewId()
        self.ctrl_2_item = find_menu.Append(ctrl_2_item_id, self.__get_menu_text('ctrl_2'), '')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_ctrl_2, self.ctrl_2_item)

        ctrl_3_item_id = wx.NewId()
        self.ctrl_3_item = find_menu.Append(ctrl_3_item_id, self.__get_menu_text('ctrl_3'), '')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_ctrl_3, self.ctrl_3_item)

        ctrl_4_item_id = wx.NewId()
        self.ctrl_4_item = find_menu.Append(ctrl_4_item_id, self.__get_menu_text('ctrl_4'), '')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_ctrl_4, self.ctrl_4_item)

        ctrl_5_item_id = wx.NewId()
        self.ctrl_5_item = find_menu.Append(ctrl_5_item_id, self.__get_menu_text('ctrl_5'), '')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_ctrl_5, self.ctrl_5_item)

        ctrl_6_item_id = wx.NewId()
        self.ctrl_6_item = find_menu.Append(ctrl_6_item_id, self.__get_menu_text('ctrl_6'), '')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_ctrl_6, self.ctrl_6_item)

        ctrl_7_item_id = wx.NewId()
        self.ctrl_7_item = find_menu.Append(ctrl_7_item_id, self.__get_menu_text('ctrl_7'), '')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_ctrl_7, self.ctrl_7_item)

        ctrl_8_item_id = wx.NewId()
        self.ctrl_8_item = find_menu.Append(ctrl_8_item_id, self.__get_menu_text('ctrl_8'), '')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_ctrl_8, self.ctrl_8_item)

        ctrl_9_item_id = wx.NewId()
        self.ctrl_9_item = find_menu.Append(ctrl_9_item_id, self.__get_menu_text('ctrl_9'), '')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_ctrl_9, self.ctrl_9_item)

        ctrl_0_item_id = wx.NewId()
        self.ctrl_0_item = find_menu.Append(ctrl_0_item_id, self.__get_menu_text('ctrl_0'), '')
        self.parent.Bind(wx.EVT_MENU, self.parent.on_ctrl_0, self.ctrl_0_item)

        menubar.Append(find_menu, 'F&ind')

    def __get_menu_text(self, id):
        text = self.config.GetValue(id)
        if len(text) == 0:
            return "EMPTY"
        if len(text) < 10:
            return text
        return text[:10] + "..."

    def _add_view_menu(self, menubar):
        viewMenu = wx.Menu()

        showMainSearchBoxId = wx.NewId()
        self.showMainSearchBox = viewMenu.Append(showMainSearchBoxId, '&Toggle main search box', 'Toggle main search box')
        self.parent.Bind(wx.EVT_MENU, self.parent.showMainSearchBoxToggle, self.showMainSearchBox)

        FontSize14Id = wx.NewId()
        self.FontSize14 = viewMenu.Append(FontSize14Id, 'Font size 1&4', 'Set Font size 14')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSetFontSize14, self.FontSize14)

        FontSize10Id = wx.NewId()
        self.FontSize10 = viewMenu.Append(FontSize10Id, 'Font size 1&0', 'Set Font size 10')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSetFontSize10, self.FontSize10)

        FontSize8Id = wx.NewId()
        self.FontSize8 = viewMenu.Append(FontSize8Id, 'Font size &8', 'Set Font size 8')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSetFontSize8, self.FontSize8)

        bgBlackColorItemsId = wx.NewId()
        self.bgBlackColorItems = viewMenu.AppendCheckItem(bgBlackColorItemsId, 'Set Blac&k', 'Set backgourd as Black')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSetBlackColorBg, self.bgBlackColorItems)
        bgBlueColorItemsId = wx.NewId()
        self.bgBlueColorItems = viewMenu.AppendCheckItem(bgBlueColorItemsId, 'Set &Blue', 'Set backgourd as Blue')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSetBlueColorBg, self.bgBlueColorItems)
        self.bgBlueColorItems.Check(True)
        bgWhiteColorItemsId = wx.NewId()
        self.bgWhiteColorItems = viewMenu.AppendCheckItem(bgWhiteColorItemsId, 'Set &White', 'Set backgourd as White')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSetWhiteColorBg, self.bgWhiteColorItems)
        bgYellowColorItemsId = wx.NewId()
        self.bgYellowColorItems = viewMenu.AppendCheckItem(bgYellowColorItemsId, 'Set &Yellow', 'Set backgourd as Yellow')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSetYellowColorBg, self.bgYellowColorItems)
        menubar.Append(viewMenu, '&View')

    def on_toggle_view_menu(self, color):
        self.bgBlackColorItems.Check(False)
        self.bgBlueColorItems.Check(False)
        self.bgWhiteColorItems.Check(False)
        self.bgYellowColorItems.Check(False)

        if color == "BLACK":
            self.bgBlackColorItems.Check(True)
        if color == "BLUE":
            self.bgBlueColorItems.Check(True)
        if color == "WHITE":
            self.bgWhiteColorItems.Check(True)
        if color == "YELLOW":
            self.bgYellowColorItems.Check(True)

    def _add_help_menu(self, menubar):
        helpMenu = wx.Menu()
        aboutItemId = wx.NewId()
        aboutItem = helpMenu.Append(aboutItemId, '&About', 'About')
        self.parent.Bind(wx.EVT_MENU, self.parent.OnAbout, aboutItem)
        menubar.Append(helpMenu, '&Help')

    def SetValue(self, key):
        self.ctrl_0_item.SetItemLabel('Ctrl+0> ' + key['ctrl_0'])
        self.ctrl_1_item.SetItemLabel('Ctrl+1> ' + key['ctrl_1'])
        self.ctrl_2_item.SetItemLabel('Ctrl+2> ' + key['ctrl_2'])
        self.ctrl_3_item.SetItemLabel('Ctrl+3> ' + key['ctrl_3'])
        self.ctrl_4_item.SetItemLabel('Ctrl+4> ' + key['ctrl_4'])
        self.ctrl_5_item.SetItemLabel('Ctrl+5> ' + key['ctrl_5'])
        self.ctrl_6_item.SetItemLabel('Ctrl+6> ' + key['ctrl_6'])
        self.ctrl_7_item.SetItemLabel('Ctrl+7> ' + key['ctrl_7'])
        self.ctrl_8_item.SetItemLabel('Ctrl+8> ' + key['ctrl_8'])
        self.ctrl_9_item.SetItemLabel('Ctrl+9> ' + key['ctrl_9'])
