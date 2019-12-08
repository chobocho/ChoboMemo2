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
        self.text = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER|
                                              wx.TE_MULTILINE|
                                              wx.TE_READONLY|
                                              wx.TE_RICH2, 
                                size=(WINDOW_SIZE/2,WINDOW_SIZE))
        self.text.SetValue("")
        font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.text.SetFont(font)
        self.text.SetBackgroundColour((0,51,102))
        self.text.SetForegroundColour(wx.WHITE)
        sizer.Add(self.text, 1, wx.EXPAND)

        btnBox = wx.BoxSizer(wx.HORIZONTAL)

        copyBtnId = wx.NewId()
        copyBtn = wx.Button(self, copyBtnId, "Copy", size=(50,30))
        copyBtn.Bind(wx.EVT_BUTTON, self.OnCopyToClipboard)
        btnBox.Add(copyBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 1)

        sizer.Add(btnBox, 0, wx.ALIGN_CENTER_VERTICAL, 1)

        self.SetSizer(sizer)

    def OnCopyToClipboard(self, event):
        text = self.text.GetValue()
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(text))
            wx.TheClipboard.Close()
        self.logger.info('')

    def OnSetBGColor(self, bgColor, fontColor):
        self.text.SetBackgroundColour(bgColor)
        self.text.SetForegroundColour(fontColor)
        self.text.Refresh()

    def OnSetMemo(self, memo):
        self.text.SetValue(memo)