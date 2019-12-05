#!/usr/bin/python
#-*- coding: utf-8 -*-

import wx
from MemoPanel import *
from ListPanel import *
from memomenu import * 
from MemoManager import MemoManager
import logging

from Observable import Observable

WINDOW_SIZE_W = 800
WINDOW_SIZE_H = 600

class MemoUIFrame(wx.Frame, Observable):
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
        self.memoManager = MemoManager(self)

    def _addMenubar(self):
        self.menu = MemoMenu(self)

    def OnQuit(self, event):
        self.Close()

    def OnAbout(self, event):
        msg = self.swVersion + '\nhttp://chobocho.com'
        title = 'About'
        wx.MessageBox(msg, title, wx.OK | wx.ICON_INFORMATION)

    def OnUpdateMemoList(self, memoList):
        self.logger.info('.')
        self.leftPanel.OnUpdateList(memoList)

    def OnUpdateMemo(self, memoIdx):
        self.logger.info(memoIdx)
        self.rightPanel.OnSetMemo(self.memoManager.OnGetMemo(memoIdx))