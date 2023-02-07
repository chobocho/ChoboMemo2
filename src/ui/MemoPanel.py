#!/usr/bin/python
#-*- coding: utf-8 -*-

import wx
import logging

from util import textutil

WINDOW_SIZE = 480
MAX_HIGHLIGHT_POS = 128
NEXT_HOP = 8

class MemoPanel(wx.Panel):
    def __init__(self, parent, *args, **kw):
        super(MemoPanel, self).__init__(*args, **kw)
        self.logger = logging.getLogger("chobomemo")
        self.parent = parent
        self._initUi()
        self.SetAutoLayout(True)
        self.memoIdx = ""
        self.high_light_keyword_pos = []
        self.current_pos = 0
        self.pos = 0
        self.move_hop = [0]

    def _initUi(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        titleBox = wx.BoxSizer(wx.HORIZONTAL)
        self.title = wx.TextCtrl(self, style = wx.TE_READONLY,
                                 size=(WINDOW_SIZE,25))
        self.title.SetValue("")
        titleBox.Add(self.title, 1, wx.ALIGN_CENTER_VERTICAL, 1)
        sizer.Add(titleBox, 0, wx.ALIGN_LEFT)

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

        self.searchText = wx.TextCtrl(self, wx.NewId(), style = wx.TE_PROCESS_ENTER,size=(200,25))
        self.searchText.Bind(wx.EVT_TEXT_ENTER, self.OnSearchKeyword)
        self.searchText.SetValue("")
        self.searchText.SetHint("Input high light keyword~")
        btnBox.Add(self.searchText, 0, wx.ALIGN_CENTRE, 5)

        self.searchBtn = wx.Button(self, wx.NewId(), "Find", size=(50,30))
        self.searchBtn.Bind(wx.EVT_BUTTON, self.OnSearchKeyword)
        btnBox.Add(self.searchBtn, 0, wx.ALIGN_CENTRE, 5)        

        self.search_prev_btn = wx.Button(self, wx.NewId(), "<", size=(30,30))
        self.search_prev_btn.Bind(wx.EVT_BUTTON, self._on_move_prev_keyword)
        btnBox.Add(self.search_prev_btn, 0, wx.ALIGN_CENTRE, 5)

        self.search_next_btn = wx.Button(self, wx.NewId(), ">", size=(30,30))
        self.search_next_btn.Bind(wx.EVT_BUTTON, self._on_move_next_keyword)
        btnBox.Add(self.search_next_btn, 0, wx.ALIGN_CENTRE, 5)

        self.searchClearBtn = wx.Button(self, wx.NewId(), "Clear", size=(50,30))
        self.searchClearBtn.Bind(wx.EVT_BUTTON, self.OnSearchClear)
        btnBox.Add(self.searchClearBtn, 1, wx.ALIGN_CENTRE, 5)

        self.saveAsMDBtn = wx.Button(self, wx.NewId(), "Save", size=(50,30))
        self.saveAsMDBtn.Bind(wx.EVT_BUTTON, self.OnSaveAsMD)
        self.saveAsMDBtn.SetToolTip("Save current memo as a file")
        btnBox.Add(self.saveAsMDBtn, 1, wx.ALIGN_CENTRE, 5)

        sizer.Add(btnBox, 0, wx.ALIGN_LEFT, 1)

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

    def OnSetMemo(self, index, title, memo, hightlight=None):
        if hightlight is None:
            hightlight = []
        self.memoIdx = index
        self.title.SetValue(title)
        self.text.SetValue(memo)
        self.OnShowHighLight(hightlight)
        self.pos = 0
        self.move_hop = textutil.getEnterPos(memo)

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
        self.high_light_keyword_pos = [0]
        self.current_pos = 0

        if len(highLightPosition) >= MAX_HIGHLIGHT_POS:
            self.logger.info('{0} is too many. Reudce to {1}'.format(len(highLightPosition), MAX_HIGHLIGHT_POS))
            highLightPosition = highLightPosition[:MAX_HIGHLIGHT_POS]

        for pos in highLightPosition:
            self.text.SetStyle(pos[0], pos[1], wx.TextAttr(wx.BLACK,"Light blue"))
            self.high_light_keyword_pos.append(pos[0])

        if (len(self.high_light_keyword_pos) > 1):
            self.current_pos = 1

        #self.__set_focus()

    def __set_focus(self):
        self.text.SetInsertionPoint(self.high_light_keyword_pos[self.current_pos])
        self.text.SetFocus()

    def _on_move_next_keyword(self, evnet):
        print("NEXT ", self.current_pos)
        if len(self.high_light_keyword_pos) == 0:
            return
        max_pos = len(self.high_light_keyword_pos)
        self.current_pos = (self.current_pos + 1) % max_pos
        self.__set_focus()

    def _on_move_prev_keyword(self, evnet):
        print("PREV: ", self.current_pos)
        if len(self.high_light_keyword_pos) == 0:
            return
        max_pos = len(self.high_light_keyword_pos)
        self.current_pos = (self.current_pos - 1 + max_pos) % max_pos
        self.__set_focus()

    def OnSaveAsMD(self, evnet):
        if len(self.memoIdx) == 0:
            return
        self.parent.OnSaveMD(self.memoIdx)

    def OnSetFontSize(self, font_size):
        font = wx.Font(font_size, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL)
        self.text.SetFont(font)

    def move_home(self):
        self.text.SetInsertionPoint(0)
        self.text.SetFocus()

    def move_end(self):
        self.text.SetInsertionPoint(len(self.text.GetValue()))
        self.text.SetFocus()

    def move_forward(self):
        pos_end = len(self.move_hop) - 1
        self.pos = self.pos + NEXT_HOP
        self.pos = self.pos if self.pos < pos_end else pos_end
        pos = self.move_hop[self.pos]

        self.text.SetInsertionPoint(pos)
        self.text.SetFocus()
        print(pos)

    def move_backward(self):
        self.pos = self.pos - NEXT_HOP
        self.pos = self.pos if self.pos > 0 else 0
        pos = self.move_hop[self.pos]

        self.text.SetInsertionPoint(pos)
        self.text.SetFocus()