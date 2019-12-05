#!/usr/bin/python
#-*- coding: utf-8 -*-
import wx
import logging

class ListPanel(wx.Panel):
    def __init__(self, parent, *args, **kw):
        super(ListPanel, self).__init__(*args, **kw)
        self.logger = logging.getLogger("chobomemo")
        self.parent = parent
        self._initUI()

    def _initUI(self):
        self.logger.info('.')
        sizer = wx.BoxSizer(wx.VERTICAL)

        ##
        listMngBtnBox = wx.BoxSizer(wx.HORIZONTAL)

        self.searchText = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER,size=(200,25))
        self.searchText.Bind(wx.EVT_TEXT_ENTER, self.OnSearchKeyword)
        self.searchText.SetValue("")
        listMngBtnBox.Add(self.searchText, 0, wx.ALIGN_CENTRE, 5)

        self.searchBtn = wx.Button(self, 10, "Find", size=(50,30))
        self.searchBtn.Bind(wx.EVT_BUTTON, self.OnSearchKeyword)
        listMngBtnBox.Add(self.searchBtn, 0, wx.ALIGN_CENTRE, 5)        

        self.searchClearBtn = wx.Button(self, 10, "Clear", size=(50,30))
        self.searchClearBtn.Bind(wx.EVT_BUTTON, self.OnSearchClear)
        listMngBtnBox.Add(self.searchClearBtn, 1, wx.ALIGN_CENTRE, 5)

        sizer.Add(listMngBtnBox, 0, wx.ALIGN_CENTER_VERTICAL, 1)

        ## memoListCtrl
        memoListID = wx.NewId()
        self.memoList = wx.ListCtrl(self, memoListID,
                                 style=wx.LC_REPORT
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 )
        sizer.Add(self.memoList, 1, wx.EXPAND)
        self.memoList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.memoList.InsertColumn(0, "No", width=30)
        self.memoList.InsertColumn(1, "Title", width=270)
        self.currentItem = -1

        ##
        urlMngBtnBox = wx.BoxSizer(wx.HORIZONTAL)

        self.editBtn = wx.Button(self, 10, "Edit", size=(70,30))
        #self.urlExportBtn.Bind(wx.EVT_BUTTON, self.OnExportUrlToHtml)
        urlMngBtnBox.Add(self.editBtn, 1, wx.ALIGN_CENTRE, 1)

        self.creatBtn = wx.Button(self, 10, "New", size=(70,30))
        #self.urlExportBtn.Bind(wx.EVT_BUTTON, self.OnExportUrlToHtml)
        urlMngBtnBox.Add(self.creatBtn, 1, wx.ALIGN_CENTRE, 1)

        self.urlSaveBtn = wx.Button(self, 10, "Save", size=(70,30))
        #self.urlSaveBtn.Bind(wx.EVT_BUTTON, self.OnSaveURL)
        urlMngBtnBox.Add(self.urlSaveBtn, 1, wx.ALIGN_CENTRE, 1)

        self.urlDeleteBtn = wx.Button(self, 10, "Delete", size=(70,30))
        #self.urlDeleteBtn.Bind(wx.EVT_BUTTON, self.OnDeleteURL)
        urlMngBtnBox.Add(self.urlDeleteBtn, 1, wx.ALIGN_CENTRE, 1)

        sizer.Add(urlMngBtnBox, 0, wx.ALIGN_CENTER_VERTICAL, 1)
        
        ##
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def OnSearchClear(self, event):
        self.searchText.SetValue("")

    def OnSearchKeyword(self, event):
        searchKeyword = self.searchText.GetValue()
        self.logger.info(searchKeyword)
        self.parent.OnSearchKeyword(searchKeyword)

    def OnItemSelected(self, evt):
        self.currentItem = evt.Index
        self.logger.info(self.currentItem)
        self.parent.OnUpdateMemo(self.currentItem)

    def OnUpdateList(self, memoList):
        self.logger.info('.')
        for memo in memoList:
            index = self.memoList.InsertItem(self.memoList.GetItemCount(), 1)
            self.memoList.SetItem(index, 0, str(index+1))
            self.memoList.SetItem(index, 1, memo[0])
            if index % 2 == 0:
                self.memoList.SetItemBackgroundColour(index, "Light blue")