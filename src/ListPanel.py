#!/usr/bin/python
#-*- coding: utf-8 -*-
import wx
import logging
from MemoUI import MemoDialog

class ListPanel(wx.Panel):
    def __init__(self, parent, *args, **kw):
        super(ListPanel, self).__init__(*args, **kw)
        self.logger = logging.getLogger("chobomemo")
        self.parent = parent
        self._initUI()

    def _initUI(self):
        self.logger.info('.')
        font = wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL)

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
        self.memoList.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self._OnUpdateMemo)
        self.memoList.InsertColumn(0, "No", width=40)
        self.memoList.InsertColumn(1, "Title", width=270)
        self.memoList.SetFont(font)
        self.currentItem = -1

        ##
        memoMngBtnBox = wx.BoxSizer(wx.HORIZONTAL)

        self.editMemoBtn = wx.Button(self, 10, "Edit", size=(70,30))
        self.editMemoBtn.Bind(wx.EVT_BUTTON, self._OnUpdateMemo)
        memoMngBtnBox.Add(self.editMemoBtn, 1, wx.ALIGN_CENTRE, 1)

        self.createMemoBtn = wx.Button(self, 10, "New", size=(70,30))
        self.createMemoBtn.Bind(wx.EVT_BUTTON, self._OnCreateMemo)
        memoMngBtnBox.Add(self.createMemoBtn, 1, wx.ALIGN_CENTRE, 1)

        self.memoSaveBtn = wx.Button(self, 10, "Save", size=(70,30))
        self.memoSaveBtn.Bind(wx.EVT_BUTTON, self._OnSaveMemo)
        memoMngBtnBox.Add(self.memoSaveBtn, 1, wx.ALIGN_CENTRE, 1)

        self.memoDeleteBtn = wx.Button(self, 10, "Delete", size=(70,30))
        self.memoDeleteBtn.Bind(wx.EVT_BUTTON, self._OnDeleteMemo)
        memoMngBtnBox.Add(self.memoDeleteBtn, 1, wx.ALIGN_CENTRE, 1)

        sizer.Add(memoMngBtnBox, 0, wx.ALIGN_CENTER_VERTICAL, 1)
        
        ##
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def _OnCreateMemo(self, event):
        self.OnCreateMemo()

    def OnCreateMemo(self):
        dlg = MemoDialog(None, title='Create new memo')
        if dlg.ShowModal() == wx.ID_OK:
            memo = {}
            memo['id'] = dlg.GetTopic()
            memo['memo'] = dlg.GetValue()
            self.parent.OnCreateMemo(memo)
        dlg.Destroy()

    def _OnUpdateMemo(self, event):
        self.OnUpdateMemo()

    def OnUpdateMemo(self):
        if self.currentItem < 0:
            self.logger.info("Not choosen item to update")
            return
   
        chosenItem = self.memoList.GetItem(self.currentItem, 0).GetText()
        self.logger.info(str(self.currentItem) + ':' + chosenItem)
        memo = self.parent.OnGetMemoItem(chosenItem)

        dlg = MemoDialog(None, title='Update memo')
        dlg.SetTopic(memo['id'])
        dlg.SetValue(memo['memo'])
        if dlg.ShowModal() == wx.ID_OK:
            memo['id'] = dlg.GetTopic()
            memo['memo'] = dlg.GetValue()
            self.parent.OnUpdateMemo(memo)
        dlg.Destroy()

    def _OnDeleteMemo(self, event):
        self.OnDeleteMemo()

    def OnDeleteMemo(self):
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
        self._OnSearchKeyword("")

    def OnSearchKeyword(self, event):
        searchKeyword = self.searchText.GetValue()
        self.logger.info(searchKeyword)
        self._OnSearchKeyword(searchKeyword)

    def _OnSearchKeyword(self, searchKeyword):
        self.parent.OnSearchKeyword(searchKeyword)

    def OnItemSelected(self, event):
        self.currentItem = event.Index
        self._OnItemSelected(self.currentItem)

    def _OnItemSelected(self, index):
        if self.memoList.GetItemCount() == 0:
            self.logger.info("List is empty!")
            return
        if index < 0:
            index = 0
        chosenItem = self.memoList.GetItem(index, 0).GetText()
        self.logger.info(str(index) + ':' + chosenItem)
        self.parent.OnGetMemo(chosenItem)

    def OnUpdateList(self, memoList):
        self.logger.info('.')
        self.memoList.DeleteAllItems()
        for key in memoList.keys():
            memo = memoList[key]
            index = self.memoList.InsertItem(self.memoList.GetItemCount(), 1)
            self.memoList.SetItem(index, 0, memo['index'])
            self.memoList.SetItem(index, 1, memo['id'])
            if index % 2 == 0:
                self.memoList.SetItemBackgroundColour(index, "Light blue")
    
    def _OnSaveMemo(self, event):
        self.OnSaveMemo()

    def OnSaveMemo(self):
        self.logger.info('.')
        self.parent.OnSaveMemo()
