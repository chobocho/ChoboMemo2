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
        memoMngBtnBox = wx.BoxSizer(wx.HORIZONTAL)

        self.editBtn = wx.Button(self, 10, "Edit", size=(70,30))
        #self.urlExportBtn.Bind(wx.EVT_BUTTON, self.OnExportUrlToHtml)
        memoMngBtnBox.Add(self.editBtn, 1, wx.ALIGN_CENTRE, 1)

        self.creatBtn = wx.Button(self, 10, "New", size=(70,30))
        #self.urlExportBtn.Bind(wx.EVT_BUTTON, self.OnExportUrlToHtml)
        memoMngBtnBox.Add(self.creatBtn, 1, wx.ALIGN_CENTRE, 1)

        self.memoSaveBtn = wx.Button(self, 10, "Save", size=(70,30))
        self.memoSaveBtn.Bind(wx.EVT_BUTTON, self.OnSaveMemo)
        memoMngBtnBox.Add(self.memoSaveBtn, 1, wx.ALIGN_CENTRE, 1)

        self.memoDeleteBtn = wx.Button(self, 10, "Delete", size=(70,30))
        self.memoDeleteBtn.Bind(wx.EVT_BUTTON, self.OnDeleteMemo)
        memoMngBtnBox.Add(self.memoDeleteBtn, 1, wx.ALIGN_CENTRE, 1)

        sizer.Add(memoMngBtnBox, 0, wx.ALIGN_CENTER_VERTICAL, 1)
        
        ##
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def OnDeleteMemo(self, event):
        self.logger.info(self.currentItem)
        if self.currentItem < 0:
            self.logger.info("Not choosen item to delete")
            return
        
        chosenItem = self.memoList.GetItem(self.currentItem, 0).GetText()
        title = self.memoList.GetItem(self.currentItem, 1).GetText()
        msg = 'Do you want to delete [' + chosenItem +'] ' + title
        title = 'Delete memo'
        askDeleteDialog = wx.MessageDialog(None, msg, title, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if askDeleteDialog.ShowModal() == wx.ID_YES:
           self.parent.OnDeleteMemo(chosenItem)
           self.logger.info(msg)
        askDeleteDialog.Destroy()
    
    def OnSearchClear(self, event):
        self.searchText.SetValue("")

    def OnSearchKeyword(self, event):
        searchKeyword = self.searchText.GetValue()
        self.logger.info(searchKeyword)
        self.parent.OnSearchKeyword(searchKeyword)

    def OnItemSelected(self, event):
        self.currentItem = event.Index
        chosenItem = self.memoList.GetItem(self.currentItem, 0).GetText()
        self.logger.info(str(self.currentItem) + ':' + chosenItem)
        self.parent.OnUpdateMemo(chosenItem)

    def OnUpdateList(self, memoList):
        self.logger.info('.')
        self.memoList.DeleteAllItems()
        for key in memoList.keys():
            memo = memoList[key]
            index = self.memoList.InsertItem(self.memoList.GetItemCount(), 1)
            self.memoList.SetItem(index, 0, memo[2])
            self.memoList.SetItem(index, 1, memo[0])
            if index % 2 == 0:
                self.memoList.SetItemBackgroundColour(index, "Light blue")

    def OnSaveMemo(self, event):
        self.logger.info('.')
        self.parent.OnSaveMemo()