#!/usr/bin/python
#-*- coding: utf-8 -*-

import wx
import os
from MemoPanel import *
from ListPanel import *
from memomenu import * 
from filedrop import *
import MemoManager
import logging

from Observer import Observer

WINDOW_SIZE_W = 800
WINDOW_SIZE_H = 600

class MemoUIFrame(wx.Frame, Observer):
    def __init__(self, *args, swVersion,  **kw):
        super(MemoUIFrame, self).__init__(*args, title = swVersion, **kw)
        self.logger = logging.getLogger("chobomemo")

        self.swVersion = swVersion
        self.splitter = wx.SplitterWindow(self, -1, wx.Point(0, 0), wx.Size(WINDOW_SIZE_W, WINDOW_SIZE_H), wx.SP_3D | wx.SP_BORDER)
        self.leftPanel = ListPanel(self, self.splitter)
        self.rightPanel = MemoPanel(self.splitter)
        self.splitter.SplitVertically(self.leftPanel, self.rightPanel)
        self.splitter.SetMinimumPaneSize(20)
        self.splitter.SetSashPosition(300, redraw=True)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self._addMenubar()

        filedrop = FileDrop(self)
        self.SetDropTarget(filedrop)

        self.memoManager = None

    def _addMenubar(self):
        self.menu = MemoMenu(self)
 
    def OnCallback(self, filelist):
        loadFile = filelist[0]

        if (".cfm" in loadFile.lower()) == False:
            self.logger.info(loadFile + "is not CFM file!")
            return
        if self.memoManager != None:
            self.memoManager.OnLoadFile(loadFile)
            self.SetTitle(self.swVersion + ' : ' + loadFile)

    def OnCreateMemo(self, memo):
        self.memoManager.OnCreateMemo(memo)

    def OnDeleteMemo(self, memoIdx):
        self.logger.info(memoIdx)
        self.memoManager.OnDeleteMemo(memoIdx)

    def OnUpdateMemo(self, memo):
        self.memoManager.OnUpdateMemo(memo)
        self.rightPanel.OnSetMemo(memo[1])

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

    def OnUpdateMemoList(self, memoList):
        self.logger.info('.')
        self.leftPanel.OnUpdateList(memoList)

    def OnGetMemoItem(self, memoIdx):
        self.logger.info(memoIdx)
        return self.memoManager.OnGetMemo(memoIdx)
        
    def OnGetMemo(self, memoIdx):
        self.logger.info(memoIdx)
        memo = self.memoManager.OnGetMemo(memoIdx)
        self.rightPanel.OnSetMemo(memo[1])

    def OnNotify(self, event = None):
        self.logger.info(event)
        if event == MemoManager.UPDATE_MEMO:
            self.OnUpdateMemoList(self.memoManager.OnGetMemoList())