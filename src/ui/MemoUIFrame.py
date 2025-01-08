#!/usr/bin/python
# -*- coding: utf-8 -*-
import collections
import os

import wx

from manager.QueryCache import QueryCache
from ui.AdvancedFindUI import AdvanceFindUI
from ui.ConfigSettingUI import ConfigSettingUI
from ui.MemoPanel import *
from ui.ListPanel import *
from ui.memomenu import *
from ui.filedrop import *
from manager import MemoManager
from manager import ConfigManager
from manager import ActionManager
import logging

from manager.Observer import Observer
from util.clipboardutil import on_get_uri_from_clipboard


class MemoUIFrame(wx.Frame, Observer):
    def __init__(self, *args, swVersion, **kw):
        super(MemoUIFrame, self).__init__(*args, title=swVersion, **kw)
        self.logger = logging.getLogger("chobomemo")
        self.config = ConfigManager.ConfigManager()
        self.action = ActionManager.ActionManager()
        self.swVersion = swVersion
        self.splitter = wx.SplitterWindow(self, -1, wx.Point(0, 0), wx.Size(self.config.GetValue('WINDOW_SIZE_W'),
                                                                            self.config.GetValue('WINDOW_SIZE_H')),
                                          wx.SP_3D | wx.SP_BORDER)
        self.leftPanel = ListPanel(self, self.splitter)
        self.rightPanel = MemoPanel(self, self.splitter)
        self.splitter.SplitVertically(self.leftPanel, self.rightPanel)
        self.splitter.SetMinimumPaneSize(20)
        self.splitter.SetSashPosition(300, redraw=True)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self._add_menubar()
        self._add_short_key()

        self.SetDropTarget(FileDrop(self))

        self.memoManager = None
        self.about_text = collections.OrderedDict()
        self.make_about_box()
        self.cache = QueryCache()
        self.leftPanel.on_toggle_save_btn(self.config.GetValue('save_cfm'))

    def _add_menubar(self):
        self.menu = MemoMenu(self, self.config)

    def _add_short_key(self):
        key_map = self.init_key_map()

        accel_tbl = []
        for item in key_map:
            self.Bind(wx.EVT_MENU, item["func"], id=(new_id := wx.NewId()))
            accel_tbl.append((item["key"][0], item["key"][1], new_id))

        self.SetAcceleratorTable(wx.AcceleratorTable(accel_tbl))
        self.Bind(wx.EVT_CLOSE, self.on_close_window)

    def init_key_map(self):
        key_map = []
        key_map.append({"key": (wx.ACCEL_ALT, ord('B')), "func": self.move_backward})
        key_map.append({"key": (wx.ACCEL_ALT, ord('C')), "func": self.__on_clear_filter})
        key_map.append({"key": (wx.ACCEL_ALT, ord('D')), "func": self.__on_focus_filter})
        key_map.append({"key": (wx.ACCEL_ALT, ord('E')), "func": self.move_end})
        key_map.append({"key": (wx.ACCEL_ALT, ord('F')), "func": self.move_forward})
        key_map.append({"key": (wx.ACCEL_ALT, ord('H')), "func": self.move_home})
        key_map.append({"key": (wx.ACCEL_ALT, ord('P')), "func": self.__on_open_uri_from_clipboard})
        key_map.append({"key": (wx.ACCEL_ALT, ord('U')), "func": self.rightPanel.set_focus_on_search_text})
        key_map.append({"key": (wx.ACCEL_ALT, ord('1')), "func": self.leftPanel.set_focus_on_list})
        key_map.append({"key": (wx.ACCEL_ALT, ord('2')), "func": self.rightPanel.set_focus_on_memo})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('1')), "func": self.on_ctrl_1})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('2')), "func": self.on_ctrl_2})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('3')), "func": self.on_ctrl_3})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('4')), "func": self.on_ctrl_4})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('5')), "func": self.on_ctrl_5})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('6')), "func": self.on_ctrl_6})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('7')), "func": self.on_ctrl_7})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('8')), "func": self.on_ctrl_8})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('9')), "func": self.on_ctrl_9})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('0')), "func": self.on_ctrl_0})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('C')), "func": self._OnCopyTitle})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('E')), "func": self._OnUpdateMemo})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('F')), "func": self.on_advanced_find})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('G')), "func": self._on_open_uri})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('M')), "func": self._OnPressCtrlM})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('N')), "func": self._on_create_memo})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('P')), "func": self._OnPressCtrlP})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('R')), "func": self.on_rename_topic})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('U')), "func": self._OnUpdateMemo})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('S')), "func": self._OnSaveMemo})
        key_map.append({"key": (wx.ACCEL_CTRL, ord('Q')), "func": self.on_close_window})
        key_map.append({"key": (wx.ACCEL_ALT | wx.ACCEL_SHIFT, ord('I')), "func": self.OnAbout})
        key_map.append({"key": (wx.ACCEL_ALT | wx.ACCEL_SHIFT, ord('C')), "func": self.on_clone_memo})
        key_map.append({"key": (wx.ACCEL_ALT | wx.ACCEL_SHIFT, ord('E')), "func": self.on_set_config_menu})
        key_map.append({"key": (wx.ACCEL_CTRL | wx.ACCEL_ALT, ord('C')), "func": self.rightPanel.OnSearchClear})
        key_map.append({"key": (wx.ACCEL_CTRL | wx.ACCEL_ALT, ord('L')), "func": self._on_toggle_search_lock})
        key_map.append({"key": (wx.ACCEL_CTRL | wx.ACCEL_ALT, ord('D')), "func": self._OnDeleteMemo})
        key_map.append({"key": (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('S')), "func": self.on_display_random_story})
        return key_map

    def OnCallback(self, filelist):
        """
        When drag & drop a file, called this function
        """
        loadFile = filelist[0]
        loadFile_lower_name = loadFile.lower()
        print(loadFile_lower_name)

        if self.memoManager is None:
            return

        allow_file_name = ['.txt', '.py', '.java', '.cpp']

        if ".cfm" not in loadFile_lower_name:
            for name in allow_file_name:
                if name in loadFile_lower_name:
                    self.memoManager.OnAddItemFromTextFile(loadFile)
                    return

            self.memoManager.on_add_item_by_files(filelist)
            self.logger.info(loadFile + " is not CFM file!")
            return

        if ".db" in loadFile.lower():
            self.memoManager.OnLoadDB()
        else:
            self.memoManager.OnLoadFile(loadFile)
        self.SetTitle(self.swVersion + ' : ' + loadFile)

    def on_toggle_edit_mode(self, event):
        self.rightPanel.on_revert_edit_mode()

    def _OnCopyTitle(self, event):
        self.leftPanel.on_copy_title()

    def _on_create_memo(self, event):
        self.leftPanel.on_create_memo()

    def _OnUpdateMemo(self, event):
        self.leftPanel.on_update_memo()

    def on_rename_topic(self, event):
        topic = self.leftPanel.get_topic()
        if topic is None:
            return

        title = 'Input new topic'
        msg = ""

        rename_dialog = wx.TextEntryDialog(None, msg, title, style = wx.OK|wx.CANCEL)
        rename_dialog.SetValue(topic)
        rename_dialog.SetMaxLength(128)
        new_topic = ""
        if rename_dialog.ShowModal() == wx.ID_OK:
            new_topic = rename_dialog.GetValue()
        rename_dialog.Destroy()

        if len(new_topic) == 0 or new_topic == topic:
            return
        self.leftPanel.update_topic(new_topic)


    def _OnDeleteMemo(self, event):
        self.leftPanel.on_delete_memo()

    def _OnSaveMemo(self, event):
        self.OnSaveMemo()

    def OnSaveMemo(self):
        self.memoManager.OnSave()

    def on_set_max_list(self, event):
        maxCount = self.leftPanel.get_max_list_count()

        dlg = wx.TextEntryDialog(None, 'Set max display list count', 'Count')
        dlg.SetValue(str(maxCount))

        if dlg.ShowModal() == wx.ID_OK:
            count = dlg.GetValue()
            count = count.strip()
            if len(count) > 0:
                try:
                    maxCount = int(count)
                    if maxCount < 0 or maxCount > 20000:
                        maxCount = 42
                except:
                    maxCount = 42
        dlg.Destroy()
        self.logger.info(maxCount)
        self.leftPanel.set_max_list_count(maxCount)

    def OnFind(self, event):
        dlg = wx.TextEntryDialog(None, 'Input keyword', 'Find')
        dlg.SetValue("")

        if dlg.ShowModal() == wx.ID_OK:
            input_keyword = dlg.GetValue()
            keyword = input_keyword.strip()
            self.OnSearchKeyword(keyword)
        dlg.Destroy()

    def on_advanced_find(self, event):
        self.run_advanced_find()

    def run_advanced_find(self):
        user_memo = self.config.GetValue('memo').split('\n')
        dlg = AdvanceFindUI(None, title='Input search keyword', ctrl_btn_list=self.config.get_ctrl_value(),
                            recent_item_list=self.cache.get(), user_memo_list=user_memo)

        if dlg.ShowModal() != wx.ID_CANCEL:
            input_keyword = dlg.GetValue()
            keyword = input_keyword.strip()
            self.OnSearchKeyword(keyword)

        is_update, user_memo = dlg.on_get_user_memo()
        dlg.Destroy()
        if is_update:
            self.config.SetMemo('\n'.join(user_memo))

    def on_display_random_story(self, event):
        self.memoManager.on_display_random_story()

    def _OnFindMemo(self, event):
        keyword = self.config.GetValue('ctrl_1')
        if len(keyword) == 0:
            return
        self._on_find_memo_by_keyword(keyword)

    def _on_find_memo_by_keyword(self, value):
        if len(value) == 0:
            return
        self.OnSearchKeyword(value)

    def _on_open_uri(self, event):
        self.leftPanel.open_uri()

    def _on_toggle_search_lock(self, event):
        self.leftPanel.on_toggle_search_lock()

    def on_set_config_menu(self, event):
        filter_item = {
            'ctrl_0': self.config.GetValue('ctrl_0'),
            'ctrl_1': self.config.GetValue('ctrl_1'),
            'ctrl_2': self.config.GetValue('ctrl_2'),
            'ctrl_3': self.config.GetValue('ctrl_3'),
            'ctrl_4': self.config.GetValue('ctrl_4'),
            'ctrl_5': self.config.GetValue('ctrl_5'),
            'ctrl_6': self.config.GetValue('ctrl_6'),
            'ctrl_7': self.config.GetValue('ctrl_7'),
            'ctrl_8': self.config.GetValue('ctrl_8'),
            'ctrl_9': self.config.GetValue('ctrl_9'),
            'ctrl_i': self.config.GetValue('ctrl_i'),
            'memo': self.config.GetValue('memo'),
            'ask_before_quit': self.config.GetValue('ask_before_quit'),
            'compressedSave': self.config.GetValue('compressedSave'),
            'save_cfm': self.config.GetValue('save_cfm')
        }

        dlg = ConfigSettingUI(None, title='Set configuration')
        dlg.SetValue(filter_item)

        is_updated = False
        if dlg.ShowModal() == wx.ID_OK:
            filter_item = dlg.GetValue()
            is_updated = True
        dlg.Destroy()

        if is_updated:
            self.config.SetValue(filter_item)
            self.menu.SetValue(filter_item)
            self.leftPanel.on_toggle_save_btn(filter_item['save_cfm'])

    def on_ctrl_i(self, event):
        keyword = self.config.GetValue('ctrl_i')
        self._on_find_memo_by_keyword(keyword)

    def on_ctrl_1(self, event):
        keyword = self.config.GetValue('ctrl_1')
        self._on_find_memo_by_keyword(keyword)

    def on_ctrl_2(self, event):
        keyword = self.config.GetValue('ctrl_2')
        self._on_find_memo_by_keyword(keyword)

    def on_ctrl_3(self, event):
        keyword = self.config.GetValue('ctrl_3')
        self._on_find_memo_by_keyword(keyword)

    def on_ctrl_4(self, event):
        keyword = self.config.GetValue('ctrl_4')
        self._on_find_memo_by_keyword(keyword)

    def on_ctrl_5(self, event):
        keyword = self.config.GetValue('ctrl_5')
        self._on_find_memo_by_keyword(keyword)

    def on_ctrl_6(self, event):
        keyword = self.config.GetValue('ctrl_6')
        self._on_find_memo_by_keyword(keyword)

    def on_ctrl_7(self, event):
        keyword = self.config.GetValue('ctrl_7')
        self._on_find_memo_by_keyword(keyword)

    def on_ctrl_8(self, event):
        keyword = self.config.GetValue('ctrl_8')
        self._on_find_memo_by_keyword(keyword)

    def on_ctrl_9(self, event):
        keyword = self.config.GetValue('ctrl_9')
        self._on_find_memo_by_keyword(keyword)

    def on_ctrl_0(self, event):
        keyword = self.config.GetValue('ctrl_0')
        self._on_find_memo_by_keyword(keyword)

    def on_create_memo(self, memo):
        self.memoManager.on_create_memo(memo)

    def OnDeleteMemo(self, memo_idx):
        self.logger.info(memo_idx)
        self.memoManager.on_delete_memo(memo_idx)

    def save_memo_panel(self):
        print(">> save_memo_panel <<")
        if self.rightPanel.is_edit_mode():
            self.rightPanel.save_memo()

    def is_edit_mode(self):
        return self.rightPanel.is_edit_mode()

    def OnUpdateMemo(self, memo):
        self.on_update_memo(memo)
        self.rightPanel.OnSetMemo(memo['index'], memo['id'], memo['memo'], memo['highlight'])

    def on_update_memo(self, memo):
        self.memoManager.OnUpdateMemo(memo)

    def OnSetMemoManager(self, memo_manager):
        self.memoManager = memo_manager
        self.memoManager.set_split_op(self.config.GetValue("AND"), self.config.GetValue("OR"))
        self.memoManager.set_save_mode(self.config.GetValue("compressedSave"), self.config.GetValue('save_cfm'))

    def OnSaveFilteredItems(self, event):
        export_file_path = ""
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile="", wildcard="Cfm files (*.cfm)|*.cfm", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )

        if dlg.ShowModal() == wx.ID_OK:
            export_file_path = dlg.GetPath()
            self.memoManager.OnSave(filter=".", filename=export_file_path)
        dlg.Destroy()

    def OnQuit(self, event):
        self.Close()

    def on_close_window(self, event):
        try:
            self.save_memo_panel()
            self.config.save()
            if self.cache.is_need_to_save:
                self.cache.save()
        except:
            ...
        if self.config.GetValue('ask_before_quit'):
            if wx.MessageBox('Do you want to finish?', 'Minim', wx.YES_NO) != wx.YES:
                event.Skip(False)
                return
        self.Destroy()

    def OnSetBlackColorBg(self, event):
        self.rightPanel.OnSetBGColor(wx.BLACK, wx.WHITE)
        self.menu.on_toggle_view_menu("BLACK")

    def OnSetBlueColorBg(self, event):
        self._on_set_blue_color_bg()

    def _on_set_blue_color_bg(self):
        self.rightPanel.OnSetBGColor((0, 51, 102), wx.WHITE)
        self.menu.on_toggle_view_menu("BLUE")

    def OnSetYellowColorBg(self, event):
        self.rightPanel.OnSetBGColor((255, 255, 204), wx.BLACK)
        self.menu.on_toggle_view_menu("YELLOW")

    def OnSetWhiteColorBg(self, event):
        self._on_set_white_color_bg()

    def _on_set_white_color_bg(self):
        self.rightPanel.OnSetBGColor(wx.WHITE, wx.BLACK)
        self.menu.on_toggle_view_menu("WHITE")

    def make_about_box(self):
        self.about_text['Alt +P'] = "Open URL in clipboard\n"
        self.about_text['Ctrl+N'] = "Create memo"
        self.about_text['Ctrl+E'] = "Toggle edit mode"
        self.about_text['Ctrl+U'] = "Edit memo"
        self.about_text['Ctrl+Alt+D'] = "Delete memo"
        self.about_text['Ctrl+Shift+C'] = "Clone memo"
        self.about_text['Alt+Shift+C'] = "Clone memo\n"
        self.about_text['Ctrl+Shift+I'] = "Display this windows"
        self.about_text['Alt+Shift+I'] = "Display this windows\n"
        self.about_text['Ctrl+Shift+E'] = "Set configuration"
        self.about_text['Alt+Shift+E'] = "Set configuration\n"
        self.about_text['Ctrl+Shift+S'] = "Display 20 random items\n"
        self.about_text['Ctrl+F'] = "Find memo\n"
        self.about_text['Ctrl+Shift+F'] = "Simple Find memo"
        self.about_text['Ctrl+S'] = "Save"
        self.about_text['Ctrl+Q'] = "Quit\n"
        self.about_text['Ctrl+M'] = "Run Notepad"
        self.about_text['Ctrl+P'] = "Run MsPaint"

    def OnAbout(self, event):
        help_text_data = ""
        for k,v in self.about_text.items():
            help_text_data += f"{k} : {v}\n"

        planner = 'Planner: NH._.K'
        developer = "Dev: chobocho.com"
        homepage = f"-------------------------------------\n"
        msg = f"Minim\n\n{help_text_data}\n{homepage}{developer}\n{planner}"
        title = 'About'
        wx.MessageBox(msg, title, wx.OK | wx.ICON_INFORMATION)

    def OnSearchKeyword(self, search_keyword):
        search_keyword_list = search_keyword

        if (len(search_keyword) > 1) and (search_keyword[-1] == '.'):
            self.OnSearchKeywordInTitle(search_keyword[:-1])
            return
        elif (len(search_keyword) > 1) and (search_keyword[0] == '`'):
            self.OnSearchKeywordInTitle(search_keyword[1:])
            return
        elif (len(search_keyword) > 1) and (search_keyword[0] == "'"):
            self.OnSearchKeywordInTitle(search_keyword[1:])
            return
        elif (len(search_keyword) > 2) and (search_keyword[:2].lower() == 't:'):
            self.OnSearchKeywordInTitle(search_keyword[2:])
            return

        print(search_keyword_list)
        self.cache.add(search_keyword)
        self.memoManager.OnSetFilter(search_keyword_list)
        # self.rightPanel.OnSetSearchKeyword(searchKeyword)
        self.leftPanel.OnItemSelected(0)
        self.leftPanel.on_set_filter_keyword(search_keyword)

    def OnSearchKeywordInTitle(self, search_keyword):
        search_keyword_list = search_keyword
        self.cache.add(search_keyword)
        print(f'OnSearchKeywordInTitle> {search_keyword_list}')
        self.memoManager.OnSetFilterInTitle(search_keyword_list)
        # self.rightPanel.OnSetSearchKeyword(searchKeyword)
        self.leftPanel.OnItemSelected(0)
        self.leftPanel.on_set_filter_keyword(search_keyword)

    def OnUpdateMemoList(self, memo_list):
        self.logger.info('.')
        self.leftPanel.on_update_list(memo_list)

    def OnGetMemoItem(self, memo_idx, search_keyword=""):
        self.logger.info(memo_idx + ":" + search_keyword)
        return self.memoManager.OnGetMemo(memo_idx, search_keyword)

    def OnGetMemo(self, memo_idx):
        self.logger.info(memo_idx)
        search_keyword = self.rightPanel.OnGetSearchKeyword()
        memo = self.memoManager.OnGetMemo(memo_idx, search_keyword)
        self.rightPanel.OnSetMemo(memo['index'], memo['id'], memo['memo'], memo['highlight'])

    def OnNotify(self, event=None):
        self.logger.info(event)
        if event == MemoManager.UPDATE_MEMO:
            self.OnUpdateMemoList(self.memoManager.OnGetMemoList())

    def OnSaveMD(self, memoIdx):
        self.logger.info(memoIdx)

        export_file_path = ""
        dlg = wx.FileDialog(
            self, message="Save file as markdown", defaultDir=os.getcwd(),
            defaultFile="", wildcard="md files (*.md)|*.md", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )

        if dlg.ShowModal() == wx.ID_OK:
            export_file_path = dlg.GetPath()
            self.memoManager.OnSaveAsMD(memoIdx, filename=export_file_path)
        dlg.Destroy()

    def _OnPressCtrlP(self, event):
        self.action.OnRunCommand("ctrl_p")

    def _OnPressCtrlM(self, event):
        self.action.OnRunCommand("ctrl_m")

    def __on_open_uri_from_clipboard(self, event):
        uri = on_get_uri_from_clipboard()
        # print(uri)

        if len(uri) == 0:
            return

        if (len(uri) <= 3) or ("http" not in uri.lower()):
            if webutil.is_special_uri(uri):
                webutil.open_uri(uri)
                return

        if len(uri) > 3:
            webutil.open_uri(uri)

    def __on_clear_filter(self, event):
        self.leftPanel.on_clear_filter()

    def __on_focus_filter(self, event):
        self.leftPanel.on_focus_filter()

    def on_clone_memo(self, event):
        self.save_memo_panel()
        self.leftPanel.on_clone_memo()

    def OnCloneMemo(self, memoIdx):
        self.memoManager.OnCloneMemo(memoIdx)

    def OnSetFontSize14(self, event):
        self.__OnSetFontSize(14)

    def OnSetFontSize10(self, event):
        self.__OnSetFontSize(10)

    def OnSetFontSize8(self, event):
        self.__OnSetFontSize(8)

    def __OnSetFontSize(self, font_size):
        self.rightPanel.OnSetFontSize(font_size)
        self._on_set_white_color_bg()
        self._on_set_blue_color_bg()

    def move_home(self, event):
        self.rightPanel.move_home()

    def move_end(self, event):
        self.rightPanel.move_end()

    def move_forward(self, event):
        self.rightPanel.move_forward()

    def move_backward(self, event):
        self.rightPanel.move_backward()
