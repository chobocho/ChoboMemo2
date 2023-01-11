#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import wx

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
        self._addMenubar()
        self._addShortKey()

        filedrop = FileDrop(self)
        self.SetDropTarget(filedrop)

        self.memoManager = None

    def _addMenubar(self):
        self.menu = MemoMenu(self, self.config)

    def _addShortKey(self):
        ctrl_C_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnCopyTitle, id=ctrl_C_Id)
        ctrl_D_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnDeleteMemo, id=ctrl_D_Id)
        ctrl_E_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnUpdateMemo, id=ctrl_E_Id)
        ctrl_U_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnUpdateMemoAndOpen, id=ctrl_U_Id)
        ctrl_F_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.OnFind, id=ctrl_F_Id)
        ctrl_G_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._on_open_uri, id=ctrl_G_Id)
        ctrl_N_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnCreateMemo, id=ctrl_N_Id)

        ctrl_P_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnPressCtrlP, id=ctrl_P_Id)
        ctrl_R_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnPressCtrlR, id=ctrl_R_Id)

        ctrl_M_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnPressCtrlM, id=ctrl_M_Id)

        ctrl_Q_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.OnQuit, id=ctrl_Q_Id)
        ctrl_S_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnSaveMemo, id=ctrl_S_Id)

        ctrl_1_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnFindMemo, id=ctrl_1_Id)

        ctrl_2_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.on_ctrl_2, id=ctrl_2_Id)
        ctrl_3_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.on_ctrl_3, id=ctrl_3_Id)
        ctrl_4_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.on_ctrl_4, id=ctrl_4_Id)
        ctrl_5_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.on_ctrl_5, id=ctrl_5_Id)
        ctrl_6_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.on_ctrl_6, id=ctrl_6_Id)
        ctrl_7_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.on_ctrl_7, id=ctrl_7_Id)
        ctrl_8_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.on_ctrl_8, id=ctrl_8_Id)
        ctrl_9_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.on_ctrl_9, id=ctrl_9_Id)
        ctrl_0_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.on_ctrl_0, id=ctrl_0_Id)

        clear_filter_id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.__on_clear_filter, id=clear_filter_id)

        focus_filter_id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.__on_focus_filter, id=focus_filter_id)

        alt_p_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.__on_open_uri_from_clipboard, id=alt_p_Id)

        move_home_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.move_home, id=move_home_id)

        move_end_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.move_end, id=move_end_id)

        move_forward_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.move_forward, id=move_forward_id)

        move_backward_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.move_backward, id=move_backward_id)

        on_clone_item_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.on_clone_memo, id=on_clone_item_id)

        on_edit_filter_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.on_set_config_menu, id=on_edit_filter_id)

        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_ALT, ord('B'), move_backward_id),
            (wx.ACCEL_ALT, ord('C'), clear_filter_id),
            (wx.ACCEL_ALT, ord('D'), focus_filter_id),
            (wx.ACCEL_ALT, ord('E'), move_end_id),
            (wx.ACCEL_ALT, ord('F'), move_forward_id),
            (wx.ACCEL_ALT, ord('H'), move_home_id),
            (wx.ACCEL_ALT, ord('P'), alt_p_Id),
            (wx.ACCEL_CTRL, ord('1'), ctrl_1_Id),
            (wx.ACCEL_CTRL, ord('2'), ctrl_2_Id),
            (wx.ACCEL_CTRL, ord('3'), ctrl_3_Id),
            (wx.ACCEL_CTRL, ord('4'), ctrl_4_Id),
            (wx.ACCEL_CTRL, ord('5'), ctrl_5_Id),
            (wx.ACCEL_CTRL, ord('6'), ctrl_6_Id),
            (wx.ACCEL_CTRL, ord('7'), ctrl_7_Id),
            (wx.ACCEL_CTRL, ord('8'), ctrl_8_Id),
            (wx.ACCEL_CTRL, ord('9'), ctrl_9_Id),
            (wx.ACCEL_CTRL, ord('0'), ctrl_0_Id),
            (wx.ACCEL_CTRL, ord('C'), ctrl_C_Id),
            (wx.ACCEL_CTRL, ord('D'), ctrl_D_Id),
            (wx.ACCEL_CTRL, ord('E'), ctrl_E_Id),
            (wx.ACCEL_CTRL, ord('F'), ctrl_F_Id),
            (wx.ACCEL_CTRL, ord('G'), ctrl_G_Id),
            (wx.ACCEL_CTRL, ord('M'), ctrl_M_Id),
            (wx.ACCEL_CTRL, ord('N'), ctrl_N_Id),
            (wx.ACCEL_CTRL, ord('P'), ctrl_P_Id),
            (wx.ACCEL_CTRL, ord('R'), ctrl_R_Id),
            (wx.ACCEL_CTRL, ord('U'), ctrl_U_Id),
            (wx.ACCEL_CTRL, ord('S'), ctrl_S_Id),
            (wx.ACCEL_CTRL, ord('Q'), ctrl_Q_Id),
            (wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord('C'), on_clone_item_id),
            (wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord('E'), on_edit_filter_id)])

        self.SetAcceleratorTable(accel_tbl)

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

            self.memoManager.OnAddItemByFiles(filelist)
            self.logger.info(loadFile + " is not CFM file!")
            return

        if ".db" in loadFile.lower():
            self.memoManager.OnLoadDB()
        else:
            self.memoManager.OnLoadFile(loadFile)
        self.SetTitle(self.swVersion + ' : ' + loadFile)

    def _OnCopyTitle(self, event):
        self.leftPanel.on_copy_title()

    def _OnCreateMemo(self, event):
        self.leftPanel.OnCreateMemo()

    def _OnUpdateMemo(self, event):
        self.leftPanel.OnUpdateMemo()

    def _OnUpdateMemoAndOpen(self, event):
        self.leftPanel.open_uri()
        self.leftPanel.OnUpdateMemo()

    def _OnDeleteMemo(self, event):
        self.leftPanel.OnDeleteMemo()

    def _OnSaveMemo(self, event):
        self.OnSaveMemo()

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

    def _OnFindMemo(self, event):
        keyword = self.config.GetValue('ctrl_1')
        if len(keyword) == 0:
            return
        self.__OnFindMemo(keyword)

    def __OnFindMemo(self, value):
        if len(value) == 0:
            return
        self.OnSearchKeyword(value)

    def _on_open_uri(self, event):
        self.leftPanel.open_uri()

    def on_set_config_menu(self, event):
        filter_item = {
            'ctrl_0' : self.config.GetValue('ctrl_0'),
            'ctrl_1' : self.config.GetValue('ctrl_1'),
            'ctrl_2' : self.config.GetValue('ctrl_2'),
            'ctrl_3' : self.config.GetValue('ctrl_3'),
            'ctrl_4' : self.config.GetValue('ctrl_4'),
            'ctrl_5' : self.config.GetValue('ctrl_5'),
            'ctrl_6' : self.config.GetValue('ctrl_6'),
            'ctrl_7' : self.config.GetValue('ctrl_7'),
            'ctrl_8' : self.config.GetValue('ctrl_8'),
            'ctrl_9' : self.config.GetValue('ctrl_9'),
            'ctrl_i' : self.config.GetValue('ctrl_i')
        }

        dlg = ConfigSettingUI(None, title='Set filter items')
        dlg.SetValue(filter_item)

        is_updated = False
        if dlg.ShowModal() == wx.ID_OK:
            filter_item = dlg.GetValue()
            is_updated = True
        dlg.Destroy()

        if is_updated:
            self.config.SetValue(filter_item)
            self.config.save()
            self.menu.SetValue(filter_item)

    def on_ctrl_1(self, event):
        keyword = self.config.GetValue('ctrl_1')
        self.__OnFindMemo(keyword)

    def on_ctrl_2(self, event):
        keyword = self.config.GetValue('ctrl_2')
        self.__OnFindMemo(keyword)

    def on_ctrl_3(self, event):
        keyword = self.config.GetValue('ctrl_3')
        self.__OnFindMemo(keyword)

    def on_ctrl_4(self, event):
        keyword = self.config.GetValue('ctrl_4')
        self.__OnFindMemo(keyword)

    def on_ctrl_5(self, event):
        keyword = self.config.GetValue('ctrl_5')
        self.__OnFindMemo(keyword)

    def on_ctrl_6(self, event):
        keyword = self.config.GetValue('ctrl_6')
        self.__OnFindMemo(keyword)

    def on_ctrl_7(self, event):
        keyword = self.config.GetValue('ctrl_7')
        self.__OnFindMemo(keyword)

    def on_ctrl_8(self, event):
        keyword = self.config.GetValue('ctrl_8')
        self.__OnFindMemo(keyword)

    def on_ctrl_9(self, event):
        keyword = self.config.GetValue('ctrl_9')
        self.__OnFindMemo(keyword)

    def on_ctrl_0(self, event):
        keyword = self.config.GetValue('ctrl_0')
        self.__OnFindMemo(keyword)

    def OnCreateMemo(self, memo):
        self.memoManager.OnCreateMemo(memo)

    def OnDeleteMemo(self, memoIdx):
        self.logger.info(memoIdx)
        self.memoManager.OnDeleteMemo(memoIdx)

    def OnUpdateMemo(self, memo):
        self.memoManager.OnUpdateMemo(memo)
        self.rightPanel.OnSetMemo(memo['index'], memo['id'], memo['memo'], memo['highlight'])

    def OnSetMemoManager(self, memoManager):
        self.memoManager = memoManager
        self.memoManager.set_split_op(self.config.GetValue("AND"), self.config.GetValue("OR"))
        self.memoManager.set_save_mode(self.config.GetValue("compressedSave") == "true")

    def OnSaveFilteredItems(self, event):
        exportFilePath = ""
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile="", wildcard="Cfm files (*.cfm)|*.cfm", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )

        if dlg.ShowModal() == wx.ID_OK:
            exportFilePath = dlg.GetPath()
            self.memoManager.OnSave(filter=".", filename=exportFilePath)
        dlg.Destroy()

    def OnQuit(self, event):
        self.Close()

    def OnSetBlackColorBg(self, event):
        self.rightPanel.OnSetBGColor(wx.BLACK, wx.WHITE)
        self.menu.on_toggle_view_menu("BLACK")

    def OnSetBlueColorBg(self, event):
        self.__OnSetBlueColorBg()

    def __OnSetBlueColorBg(self):
        self.rightPanel.OnSetBGColor((0, 51, 102), wx.WHITE)
        self.menu.on_toggle_view_menu("BLUE")

    def OnSetYellowColorBg(self, event):
        self.rightPanel.OnSetBGColor((255, 255, 204), wx.BLACK)
        self.menu.on_toggle_view_menu("YELLOW")

    def OnSetWhiteColorBg(self, event):
        self.__OnSetWhiteColorBg()

    def __OnSetWhiteColorBg(self):
        self.rightPanel.OnSetBGColor(wx.WHITE, wx.BLACK)
        self.menu.on_toggle_view_menu("WHITE")

    def OnAbout(self, event):
        help = """
    Ctrl+N : Create memo
    Ctrl+E : Edit memo  
    Ctrl+U : Edit memo  
    Ctrl+D : Delete memo
    Ctrl+F : Find
    Ctrl+S : Save
    Ctrl+Q : Quit

    Ctrl+M : Notepad
    Ctrl+P : MsPaint

    Alt +P : Open URL in clipboard
    -------------------------------------
    http://www.chobocho.com
    """
        msg = "Minim" + '\n\n' + help + '\n\n    ' + self.swVersion
        title = 'About'
        wx.MessageBox(msg, title, wx.OK | wx.ICON_INFORMATION)

    def OnSaveMemo(self):
        self.memoManager.OnSave()

    def OnSearchKeyword(self, searchKeyword):
        search_keyword_list = searchKeyword

        if (len(searchKeyword) > 1) and (searchKeyword[-1] == '.'):
            self.OnSearchKeywordInTitle(searchKeyword[:-1])
            return
        elif (len(searchKeyword) > 1) and (searchKeyword[0] == '`'):
            self.OnSearchKeywordInTitle(searchKeyword[1:])
            return
        elif (len(searchKeyword) > 2) and (searchKeyword[:2].lower() == 't:'):
            self.OnSearchKeywordInTitle(searchKeyword[2:])
            print(searchKeyword[2:])
            return

        print(search_keyword_list)
        self.memoManager.OnSetFilter(search_keyword_list)
        # self.rightPanel.OnSetSearchKeyword(searchKeyword)
        self.leftPanel.OnItemSelected(0)
        self.leftPanel.on_set_filter_keyword(searchKeyword)

    def OnSearchKeywordInTitle(self, searchKeyword):
        searchKeywordList = searchKeyword

        self.logger.info(searchKeywordList)
        self.memoManager.OnSetFilterInTitle(searchKeywordList)
        # self.rightPanel.OnSetSearchKeyword(searchKeyword)
        self.leftPanel.OnItemSelected(0)
        self.leftPanel.on_set_filter_keyword(searchKeyword)

    def OnUpdateMemoList(self, memoList):
        self.logger.info('.')
        self.leftPanel.OnUpdateList(memoList)

    def OnGetMemoItem(self, memoIdx, searchKeyword=""):
        self.logger.info(memoIdx + ":" + searchKeyword)
        return self.memoManager.OnGetMemo(memoIdx, searchKeyword)

    def OnGetMemo(self, memoIdx):
        self.logger.info(memoIdx)
        searchKeyword = self.rightPanel.OnGetSearchKeyword()
        memo = self.memoManager.OnGetMemo(memoIdx, searchKeyword)
        self.rightPanel.OnSetMemo(memo['index'], memo['id'], memo['memo'], memo['highlight'])

    def OnNotify(self, event=None):
        self.logger.info(event)
        if event == MemoManager.UPDATE_MEMO:
            self.OnUpdateMemoList(self.memoManager.OnGetMemoList())

    def OnSaveMD(self, memoIdx):
        self.logger.info(memoIdx)

        exportFilePath = ""
        dlg = wx.FileDialog(
            self, message="Save file as markdown", defaultDir=os.getcwd(),
            defaultFile="", wildcard="md files (*.md)|*.md", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )

        if dlg.ShowModal() == wx.ID_OK:
            exportFilePath = dlg.GetPath()
            self.memoManager.OnSaveAsMD(memoIdx, filename=exportFilePath)
        dlg.Destroy()

    def _OnPressCtrlP(self, event):
        self.action.OnRunCommand("ctrl_p")

    def _OnPressCtrlR(self, event):
        self.leftPanel.query_recent_used_items()

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
        self.__OnSetWhiteColorBg()
        self.__OnSetBlueColorBg()

    def move_home(self, event):
        self.rightPanel.move_home()

    def move_end(self, event):
        self.rightPanel.move_end()

    def move_forward(self, event):
        self.rightPanel.move_forward()

    def move_backward(self, event):
        self.rightPanel.move_backward()
