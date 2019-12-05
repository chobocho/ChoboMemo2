#!/usr/bin/python
#-*- coding: utf-8 -*-

import wx
import logging

WINDOW_SIZE = 480

class MemoPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(MemoPanel, self).__init__(*args, **kw)
        self.logger = logging.getLogger("chobomemo")
        self._initUi()
        self.SetAutoLayout(True)

    def _initUi(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER|wx.TE_MULTILINE, size=(WINDOW_SIZE/2,WINDOW_SIZE))
        self.text.SetValue("")
        self.text.SetBackgroundColour((0,51,102))
        self.text.SetForegroundColour(wx.WHITE)
        font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.text.SetFont(font)
        sizer.Add(self.text, 1, wx.EXPAND)
        
        btnBox = wx.BoxSizer(wx.HORIZONTAL)

        clearBtnId = wx.NewId()
        clearBtn = wx.Button(self, clearBtnId, "Clear", size=(50,30))
        clearBtn.Bind(wx.EVT_BUTTON, self.OnClearBtn)
        btnBox.Add(clearBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 1)

        sizer.Add(btnBox, 0, wx.ALIGN_CENTER_VERTICAL, 1)
        self.SetSizer(sizer)

    def OnClearBtn(self, event):
        self.text.SetValue("")

    def OnSetMemo(self, memo):
        self.text.SetValue(memo)