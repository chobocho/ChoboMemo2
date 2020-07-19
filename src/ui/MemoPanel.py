#!/usr/bin/python
#-*- coding: utf-8 -*-

import wx
import logging

WINDOW_SIZE = 480

class MemoPanel(wx.Panel):
    def __init__(self, parent, *args, **kw):
        super(MemoPanel, self).__init__(*args, **kw)
        self.logger = logging.getLogger("chobomemo")
        self.parent = parent
        self._initUi()
        self.SetAutoLayout(True)
        self.memoIdx = ""

    def _initUi(self):
        sizer = wx.BoxSizer(wx.VERTICAL)


        titleBox = wx.BoxSizer(wx.HORIZONTAL)
        self.title = wx.TextCtrl(self, style = wx.TE_READONLY,
                                 size=(WINDOW_SIZE,25))
        self.title.SetValue("")
        titleBox.Add(self.title, 1, wx.ALIGN_CENTER_VERTICAL, 1)
        sizer.Add(titleBox, 0, wx.ALIGN_CENTER_VERTICAL)

        self.text = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER|
                                              wx.TE_MULTILINE|
                                              wx.TE_READONLY|
                                              wx.TE_RICH2, 
                                size=(WINDOW_SIZE/2,WINDOW_SIZE))
        self.text.SetValue("")
        font = wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL)
        self.text.SetFont(font)
        self.text.SetBackgroundColour((0,51,102))
        self.text.SetForegroundColour(wx.WHITE)
        sizer.Add(self.text, 1, wx.EXPAND)

        btnBox = wx.BoxSizer(wx.HORIZONTAL)

        copyBtnId = wx.NewId()
        copyBtn = wx.Button(self, copyBtnId, "Copy", size=(50,30))
        copyBtn.Bind(wx.EVT_BUTTON, self.OnCopyToClipboard)
        btnBox.Add(copyBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 1)

        self.searchText = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER,size=(200,25))
        self.searchText.Bind(wx.EVT_TEXT_ENTER, self.OnSearchKeyword)
        self.searchText.SetValue("")
        btnBox.Add(self.searchText, 0, wx.ALIGN_CENTRE, 5)

        self.searchBtn = wx.Button(self, 10, "Find", size=(50,30))
        self.searchBtn.Bind(wx.EVT_BUTTON, self.OnSearchKeyword)
        btnBox.Add(self.searchBtn, 0, wx.ALIGN_CENTRE, 5)        

        self.searchClearBtn = wx.Button(self, 10, "Clear", size=(50,30))
        self.searchClearBtn.Bind(wx.EVT_BUTTON, self.OnSearchClear)
        btnBox.Add(self.searchClearBtn, 1, wx.ALIGN_CENTRE, 5)

        self.saveAsMDBtn = wx.Button(self, 10, "Save", size=(50,30))
        self.saveAsMDBtn.Bind(wx.EVT_BUTTON, self.OnSaveAsMD)
        btnBox.Add(self.saveAsMDBtn, 1, wx.ALIGN_CENTRE, 5)

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

    def OnSetMemo(self, index, title, memo, hightlight = []):
        self.memoIdx = index
        self.title.SetValue(title)
        self.text.SetValue(memo)
        self.OnShowHighLight(hightlight)

    def OnSearchClear(self, event):
        self.searchText.SetValue("")

    def OnGetSearchKeyword(self):
        return self.searchText.GetValue()

    def OnSetSearchKeyword(self, keyword):
        self.searchText.SetValue(keyword)

    def OnSearchKeyword(self, event):
        self._OnSearchKeyword()

    def _OnSearchKeyword(self):
        searchKeyword = self.searchText.GetValue()
        self.logger.info(searchKeyword)
        self.parent.OnGetMemo(self.memoIdx)

    def OnShowHighLight(self, highLightPosition):
        self.logger.info(highLightPosition)
        for pos in highLightPosition:
            self.text.SetStyle(pos[0], pos[1], wx.TextAttr(wx.BLACK,"Light blue"))

    def OnSaveAsMD(self, evnet):
        if len(self.memoIdx) == 0:
            return
        self.parent.OnSaveMD(self.memoIdx)