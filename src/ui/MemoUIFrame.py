#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
from ui.MemoPanel import *
from ui.ListPanel import *
from ui.memomenu import *
from ui.filedrop import *
from manager import MemoManager
from manager import ConfigManager
from manager import ActionManager
import logging

from manager.Observer import Observer

class MemoUIFrame(wx.Frame, Observer):
    def __init__(self, *args, swVersion,  **kw):
        super(MemoUIFrame, self).__init__(*args, title = swVersion, **kw)
        self.logger = logging.getLogger("chobomemo")
        self.config = ConfigManager.ConfigManager()
        self.action = ActionManager.ActionManager()
        self.swVersion = swVersion
        self.splitter = wx.SplitterWindow(self, -1, wx.Point(0, 0), wx.Size(self.config.GetValue('WINDOW_SIZE_W'), self.config.GetValue('WINDOW_SIZE_H')), wx.SP_3D | wx.SP_BORDER)
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
        self.menu = MemoMenu(self)
 
    def _addShortKey(self):
        ctrl_D_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnDeleteMemo, id=ctrl_D_Id)
        ctrl_E_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnUpdateMemo, id=ctrl_E_Id)
        ctrl_U_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnUpdateMemo, id=ctrl_U_Id)
        ctrl_F_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.OnFind, id=ctrl_F_Id)
        ctrl_N_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnCreateMemo, id=ctrl_N_Id)

        ctrl_P_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnPressCtrlP, id=ctrl_P_Id)
        ctrl_M_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnPressCtrlM, id=ctrl_M_Id)

        ctrl_Q_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.OnQuit, id=ctrl_Q_Id)
        ctrl_S_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnSaveMemo, id=ctrl_S_Id)

        ctrl_1_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self._OnFindMemo, id=ctrl_1_Id)
                                    
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL,  ord('1'), ctrl_1_Id),
                                         (wx.ACCEL_CTRL,  ord('D'), ctrl_D_Id),
                                         (wx.ACCEL_CTRL,  ord('E'), ctrl_E_Id),
                                         (wx.ACCEL_CTRL,  ord('F'), ctrl_F_Id),
                                         (wx.ACCEL_CTRL,  ord('M'), ctrl_M_Id),
                                         (wx.ACCEL_CTRL,  ord('N'), ctrl_N_Id),
                                         (wx.ACCEL_CTRL,  ord('P'), ctrl_P_Id),
                                         (wx.ACCEL_CTRL,  ord('U'), ctrl_U_Id),
                                         (wx.ACCEL_CTRL,  ord('S'), ctrl_S_Id),
                                         (wx.ACCEL_CTRL,  ord('Q'), ctrl_Q_Id)])
        self.SetAcceleratorTable(accel_tbl)


    def OnCallback(self, filelist):
        """
        When drag & drop a file, called this function
        """

        loadFile = filelist[0]
        loadFile_lower_name = loadFile.lower()
        print(loadFile_lower_name)

        if self.memoManager == None:
            return

        allow_file_name = ['.txt', '.py', '.java', '.cpp']

        if (".cfm" not in loadFile_lower_name):
            for name in allow_file_name:
                if (name in loadFile_lower_name):
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

    def _OnCreateMemo(self, event):
        self.leftPanel.OnCreateMemo()

    def _OnUpdateMemo(self, event):
        self.leftPanel.OnUpdateMemo()

    def _OnDeleteMemo(self, event):
        self.leftPanel.OnDeleteMemo()

    def _OnSaveMemo(self, event):
        self.OnSaveMemo()

    def OnFind(self, event):
        dlg = wx.TextEntryDialog(None, 'Input keyword','Find')
        dlg.SetValue("")

        if dlg.ShowModal() == wx.ID_OK:
            keyword = dlg.GetValue()
            self.OnSearchKeyword(keyword)
        dlg.Destroy()

    def _OnFindMemo(self, event):
        keyword = self.config.GetValue('ctrl_1')
        if len(keyword) == 0:
            return
        self.OnSearchKeyword(keyword)

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

    def OnSetBlueColorBg(self, event):
        self.rightPanel.OnSetBGColor((0,51,102), wx.WHITE)

    def OnSetYellowColorBg(self, event):
        self.rightPanel.OnSetBGColor((255, 255, 204), wx.BLACK)

    def OnSetWhiteColorBg(self, event):
        self.rightPanel.OnSetBGColor(wx.WHITE, wx.BLACK)

    def OnAbout(self, event):
        msg = self.swVersion + '\nhttp://chobocho.com'
        title = 'About'
        wx.MessageBox(msg, title, wx.OK | wx.ICON_INFORMATION)

    def OnSaveMemo(self):
        self.memoManager.OnSave()

    def OnSearchKeyword(self, searchKeyword):
        self.logger.info(searchKeyword)
        self.memoManager.OnSetFilter(searchKeyword)
        self.rightPanel.OnSetSearchKeyword(searchKeyword)
        self.leftPanel._OnItemSelected(0)

    def OnUpdateMemoList(self, memoList):
        self.logger.info('.')
        self.leftPanel.OnUpdateList(memoList)

    def OnGetMemoItem(self, memoIdx, searchKeyword = ""):
        self.logger.info(memoIdx + ":" + searchKeyword)
        return self.memoManager.OnGetMemo(memoIdx, searchKeyword)

    def OnGetMemo(self, memoIdx):
        self.logger.info(memoIdx)
        searchKeyword = self.rightPanel.OnGetSearchKeyword()
        memo = self.memoManager.OnGetMemo(memoIdx, searchKeyword)
        self.rightPanel.OnSetMemo(memo['index'], memo['id'], memo['memo'], memo['highlight'])

    def OnNotify(self, event = None):
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

    def _OnPressCtrlM(self, event):
        self.action.OnRunCommand("ctrl_m")