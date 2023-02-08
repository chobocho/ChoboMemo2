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
        self._init_ui()
        self.SetAutoLayout(True)
        self.memo_idx = ""
        self.high_light_keyword_pos = []
        self.current_pos = 0
        self.pos = 0
        self.move_hop = [0]
        self.original_title = ""
        self.original_memo = ""

    def _init_ui(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self._add_title_box(sizer)
        self._add_text_box(sizer)
        self._add_button_box(sizer)
        self.SetSizer(sizer)

    def _add_button_box(self, sizer):
        btnBox = wx.BoxSizer(wx.HORIZONTAL)
        copyBtnId = wx.NewId()
        copyBtn = wx.Button(self, copyBtnId, "Copy", size=(50, 30))
        copyBtn.Bind(wx.EVT_BUTTON, self.OnCopyToClipboard)
        btnBox.Add(copyBtn, 1, wx.ALIGN_CENTRE | wx.ALL, 1)
        self.searchText = wx.TextCtrl(self, wx.NewId(), style=wx.TE_PROCESS_ENTER, size=(200, 25))
        self.searchText.Bind(wx.EVT_TEXT_ENTER, self.OnSearchKeyword)
        self.searchText.SetValue("")
        self.searchText.SetHint("Alt+U: Set focus here!")
        btnBox.Add(self.searchText, 0, wx.ALIGN_CENTRE, 5)
        self.searchBtn = wx.Button(self, wx.NewId(), "Find", size=(50, 30))
        self.searchBtn.Bind(wx.EVT_BUTTON, self.OnSearchKeyword)
        btnBox.Add(self.searchBtn, 0, wx.ALIGN_CENTRE, 5)
        self.search_prev_btn = wx.Button(self, wx.NewId(), "<", size=(30, 30))
        self.search_prev_btn.Bind(wx.EVT_BUTTON, self._on_move_prev_keyword)
        btnBox.Add(self.search_prev_btn, 0, wx.ALIGN_CENTRE, 5)
        self.search_next_btn = wx.Button(self, wx.NewId(), ">", size=(30, 30))
        self.search_next_btn.Bind(wx.EVT_BUTTON, self._on_move_next_keyword)
        btnBox.Add(self.search_next_btn, 0, wx.ALIGN_CENTRE, 5)
        self.searchClearBtn = wx.Button(self, wx.NewId(), "Clear", size=(50, 30))
        self.searchClearBtn.Bind(wx.EVT_BUTTON, self.OnSearchClear)
        btnBox.Add(self.searchClearBtn, 1, wx.ALIGN_CENTRE, 5)
        self.saveAsMDBtn = wx.Button(self, wx.NewId(), "Save", size=(50, 30))
        self.saveAsMDBtn.Bind(wx.EVT_BUTTON, self.OnSaveAsMD)
        self.saveAsMDBtn.SetToolTip("Save current memo as a file")
        btnBox.Add(self.saveAsMDBtn, 1, wx.ALIGN_CENTRE, 5)
        sizer.Add(btnBox, 0, wx.ALIGN_LEFT, 1)

    def _add_text_box(self, sizer):
        self.text = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER |
                                            wx.TE_MULTILINE |
                                            wx.TE_READONLY |
                                            wx.TE_RICH2,
                                size=(WINDOW_SIZE, WINDOW_SIZE))
        self.text.SetValue("")
        font = wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL)
        self.text.SetFont(font)
        self.text.SetBackgroundColour((0, 51, 102))
        self.text.SetForegroundColour(wx.WHITE)
        sizer.Add(self.text, 1, wx.EXPAND)

    def _add_title_box(self, sizer):
        titleBox = wx.BoxSizer(wx.HORIZONTAL)
        self.cb_edit_mode = wx.CheckBox(self, wx.NewId(), "Edit", size=(50, 25))
        self.cb_edit_mode.SetValue(False)
        self.cb_edit_mode.SetToolTip("Check for edit")
        self.cb_edit_mode.Bind(wx.EVT_CHECKBOX, self._on_toggle_edit_mode)
        titleBox.Add(self.cb_edit_mode, 0, wx.ALIGN_LEFT, 1)
        self.title = wx.TextCtrl(self, style=wx.TE_READONLY,
                                 size=(WINDOW_SIZE-50, 25))
        self.title.SetValue("")
        titleBox.Add(self.title, 1, wx.EXPAND, 1)
        sizer.Add(titleBox, 0, wx.EXPAND)

    def _on_toggle_edit_mode(self, event):
        self.on_toggle_edit_mode()

    def on_toggle_edit_mode(self):
        if len(self.memo_idx) == 0:
            self.cb_edit_mode.SetValue(False)
            return

        if self.cb_edit_mode.GetValue():
            self._on_set_edit_mode()
        else:
            self._on_set_read_mode()
            self.update_memo()
            self._OnSearchKeyword()

    def on_revert_edit_mode(self):
        self.cb_edit_mode.SetValue(not self.cb_edit_mode.GetValue())
        self.on_toggle_edit_mode()


    def is_edit_mode(self):
        return self.cb_edit_mode.GetValue()

    def update_memo(self):
        if self.original_title == self.title.GetValue() and self.original_memo == self.text.GetValue():
            return
        self.logger.info(f'{self.memo_idx}')
        memo_data = {'index': self.memo_idx, 'id': self.title.GetValue(), 'memo': self.text.GetValue(), 'highlight':[]}
        self.original_title = ""
        self.original_memo = ""
        self.parent.OnUpdateMemo(memo_data)

    def _on_set_edit_mode(self):
        self._set_edit_mode_color()
        self.title.SetEditable(True)
        self.text.SetEditable(True)

    def _on_set_read_mode(self):
        self._set_read_mode_color()
        self.title.SetEditable(False)
        self.text.SetEditable(False)
    def OnCopyToClipboard(self, event):
        text = self.text.GetValue()
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(text))
            wx.TheClipboard.Close()
        self.logger.info('')

    def OnSetBGColor(self, bg_color, font_color):
        self.text.SetBackgroundColour(bg_color)
        self.text.SetForegroundColour(font_color)
        self.text.Refresh()

    def _set_edit_mode_color(self):
        self.OnSetBGColor("Light blue", wx.BLACK)

    def _set_read_mode_color(self):
        self.parent._on_set_blue_color_bg()

    def OnSetMemo(self, index, title, memo_data, highlight=None):
        self.logger.info(f'{index}')
        if highlight is None:
            highlight = []
        self.memo_idx = index
        self.title.SetValue(title)
        self.text.SetValue(memo_data)
        self.OnShowHighLight(highlight)
        self.pos = 0
        self.move_hop = textutil.getEnterPos(memo_data)
        self.original_title = title
        self.original_memo = memo_data

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
        self.parent.OnGetMemo(self.memo_idx)

    def OnShowHighLight(self, highLightPosition):
        self.logger.info(highLightPosition)
        self.high_light_keyword_pos = [0]
        self.current_pos = 0

        if len(highLightPosition) >= MAX_HIGHLIGHT_POS:
            self.logger.info('{0} is too many. Reduce to {1}'.format(len(highLightPosition), MAX_HIGHLIGHT_POS))
            highLightPosition = highLightPosition[:MAX_HIGHLIGHT_POS]

        is_edit_mode = self.is_edit_mode()
        for pos in highLightPosition:
            if is_edit_mode:
                self.text.SetStyle(pos[0], pos[1], wx.TextAttr(wx.BLACK, wx.WHITE))
            else:
                self.text.SetStyle(pos[0], pos[1], wx.TextAttr(wx.BLACK, wx.WHITE))
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
        if len(self.memo_idx) == 0:
            return
        self.parent.OnSaveMD(self.memo_idx)

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

    def set_focus_on_search_text(self, event):
        self.searchText.SetFocus()