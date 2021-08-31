#!/usr/bin/python
#-*- coding: utf-8 -*-
import wx
import logging
from ui.MemoUI import MemoDialog
from util import webutil
from manager import memo_cache

class ListPanel(wx.Panel):
    def __init__(self, parent, *args, **kw):
        super(ListPanel, self).__init__(*args, **kw)
        self.logger = logging.getLogger("chobomemo")
        self.parent = parent
        self.max_list_count = 99
        self.cache = memo_cache.MemoCache()
        self.currentItem = -1
        self._initUI()


    def _initUI(self):
        self.logger.info('.')
        font = wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL)

        sizer = wx.BoxSizer(wx.VERTICAL)

        ##
        self.__init_main_search_ui(sizer)

        ## memoListCtrl
        memoListID = wx.NewId()
        self.memoList = wx.ListCtrl(self, memoListID,
                                 style=wx.LC_REPORT
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 )
        sizer.Add(self.memoList, 1, wx.EXPAND)
        self.memoList.Bind(wx.EVT_LIST_ITEM_SELECTED, self._OnItemSelected)
        self.memoList.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self._OnUpdateMemo)
        self.memoList.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._open_uri)
        self.memoList.InsertColumn(0, "No", width=60)
        self.memoList.InsertColumn(1, "Title", width=220)
        #self.memoList.InsertColumn(2, "Memo", width=200)
        self.memoList.SetFont(font)
        self.currentItem = -1

        ##
        memoMngBtnBox = wx.BoxSizer(wx.HORIZONTAL)

        recentUsedBtn_id = wx.NewId()
        self.recentUsedBtn = wx.Button(self, recentUsedBtn_id, "RUI", size=(60,30))
        self.recentUsedBtn.Bind(wx.EVT_BUTTON, self._query_recent_used_items)
        memoMngBtnBox.Add(self.recentUsedBtn, 1, wx.ALIGN_CENTRE, 1)

        self.editMemoBtn = wx.Button(self, 10, "Edit", size=(60,30))
        self.editMemoBtn.Bind(wx.EVT_BUTTON, self._OnUpdateMemo)
        memoMngBtnBox.Add(self.editMemoBtn, 1, wx.ALIGN_CENTRE, 1)

        self.createMemoBtn = wx.Button(self, 10, "New", size=(60,30))
        self.createMemoBtn.Bind(wx.EVT_BUTTON, self._OnCreateMemo)
        memoMngBtnBox.Add(self.createMemoBtn, 1, wx.ALIGN_CENTRE, 1)

        self.memoSaveBtn = wx.Button(self, 10, "Save", size=(60,30))
        self.memoSaveBtn.Bind(wx.EVT_BUTTON, self._OnSaveMemo)
        memoMngBtnBox.Add(self.memoSaveBtn, 1, wx.ALIGN_CENTRE, 1)

        self.memoDeleteBtn = wx.Button(self, 10, "Delete", size=(60,30))
        self.memoDeleteBtn.Bind(wx.EVT_BUTTON, self._OnDeleteMemo)
        memoMngBtnBox.Add(self.memoDeleteBtn, 1, wx.ALIGN_CENTRE, 1)

        sizer.Add(memoMngBtnBox, 0, wx.ALIGN_LEFT, 1)
        
        ##
        self.SetSizer(sizer)
        self.SetSizerAndFit(sizer, True)

    def __init_main_search_ui(self, sizer):
        main_search_box = wx.BoxSizer(wx.VERTICAL)

        self.mainSearchBtnBox = wx.BoxSizer(wx.HORIZONTAL)
        self.searchMainText = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(250, 25))
        self.searchMainText.Bind(wx.EVT_TEXT_ENTER, self.OnSearchKeyword)
        self.searchMainText.SetValue("")
        self.mainSearchBtnBox.Add(self.searchMainText, 0, wx.ALIGN_LEFT, 1)

        self.mainSearchClearBtn = wx.Button(self, 10, "&Clear", size=(50, 25))
        self.mainSearchClearBtn.Bind(wx.EVT_BUTTON, self.OnMainSearchClear)
        self.mainSearchBtnBox.Add(self.mainSearchClearBtn, 1, wx.ALIGN_CENTRE, 1)

        main_search_box.Add(self.mainSearchBtnBox, 0, wx.ALIGN_LEFT, 1)
        self.on_toggle_main_search_box()

        ##
        listMngBtnBox = wx.BoxSizer(wx.HORIZONTAL)
        self.searchText = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(200, 25))
        self.searchText.Bind(wx.EVT_TEXT_ENTER, self.OnSearchKeyword)
        self.searchText.SetValue("")
        listMngBtnBox.Add(self.searchText, 0, wx.ALIGN_CENTRE, 1)
        self.searchBtn = wx.Button(self, 10, "Find", size=(50, 25))
        self.searchBtn.Bind(wx.EVT_BUTTON, self.OnSearchKeyword)
        listMngBtnBox.Add(self.searchBtn, 0, wx.ALIGN_CENTRE, 1)
        self.searchClearBtn = wx.Button(self, 10, "Clear", size=(50, 25))
        self.searchClearBtn.Bind(wx.EVT_BUTTON, self.OnSearchClear)
        listMngBtnBox.Add(self.searchClearBtn, 1, wx.ALIGN_CENTRE, 1)

        main_search_box.Add(listMngBtnBox, 0, wx.ALIGN_LEFT, 1)
        sizer.Add(main_search_box, 0, wx.ALIGN_LEFT, 1)

    def _OnCreateMemo(self, event):
        self.OnCreateMemo()


    def OnCreateMemo(self):
        memo = {}
        memo['id'] = ''

        dlg = MemoDialog(None, title='Create new memo')
        if dlg.ShowModal() == wx.ID_OK:
            memo = {}
            memo['id'] = dlg.GetTopic()
            memo['memo'] = dlg.GetValue()
            self.parent.OnCreateMemo(memo)
        dlg.Destroy()

        title = memo['id']
        self._on_set_search_keyword(title)
        self._OnSearchKeyword(title)
        self.cache.add(title)


    def _OnUpdateMemo(self, event):
        self.OnUpdateMemo()


    def OnUpdateMemo(self):
        if not self.__HasItem():
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

        title = memo['id']
        self._on_set_search_keyword(title)
        self._OnSearchKeywordInTitle(title)
        self.cache.add(title)


    def _OnDeleteMemo(self, event):
        self.OnDeleteMemo()


    def OnDeleteMemo(self):
        self.logger.info(self.currentItem)

        if not self.__HasItem():
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

    def OnMainSearchClear(self, event):
        self.searchMainText.SetValue("")

    def OnSearchClear(self, event):
        self.on_clear_filter()

    def on_clear_filter(self):
        self.searchText.SetValue("")
        self._OnSearchKeyword("")

    def on_focus_filter(self):
        self.searchText.SetFocus()

    def OnSearchKeyword(self, event):
        searchMainKeyword = self.searchMainText.GetValue()
        searchKeyword = self.searchText.GetValue()
        self.logger.info(searchMainKeyword + '|' + searchKeyword)
        self._OnSearchKeyword(searchKeyword, searchMainKeyword)


    def on_set_filter_keyword(self, keyword):
        self._on_set_search_keyword(keyword)


    def _on_set_search_keyword(self, keyword):
        self.searchText.SetValue(keyword)


    def _OnSearchKeyword(self, searchKeyword, searchMainKeyword=""):
        self.parent.OnSearchKeyword(searchKeyword, searchMainKeyword)


    def _OnSearchKeywordInTitle(self, searchKeyword):
        self.parent.OnSearchKeywordInTitle(searchKeyword)


    def _query_recent_used_items(self, event):
        self.query_recent_used_items()


    def query_recent_used_items(self):
        query = self.cache.query()
        if len(query) == 0:
            return

        query = 't:' + query
        self.searchText.SetValue(query)
        self._OnSearchKeyword(query)


    def _OnItemSelected(self, event):
        self.currentItem = event.Index
        self.OnItemSelected(self.currentItem)


    def OnItemSelected(self, index):
        if self.memoList.GetItemCount() == 0:
            self.logger.info("List is empty!")
            return
        if index < 0:
            index = 0
        chosenItem = self.memoList.GetItem(index, 0).GetText()
        self.logger.info(str(index) + ':' + chosenItem)
        self.parent.OnGetMemo(chosenItem)


    def _open_uri(self, event):
        self.open_uri()


    def open_uri(self):
        if not self.__HasItem():
            return

        chosenItem = self.memoList.GetItem(self.currentItem, 0).GetText()
        uri = self.memoList.GetItem(self.currentItem, 1).GetText()

        self._on_set_search_keyword(uri)
        self.cache.add(uri)

        if (len(uri) <= 3) or ("http" not in uri.lower()):
            if webutil.is_special_uri(uri):
                webutil.open_uri(uri)
                return

            memo = self.parent.OnGetMemoItem(chosenItem)
            uri = self._get_uri_from_data(memo['memo'])

        if len(uri) > 3:
            webutil.open_uri(uri)


    def on_copy_title(self):
        if not self.__HasItem():
            return

        chosenItemCount = self.memoList.GetSelectedItemCount()
        nextItem = self.memoList.GetFirstSelected()

        selectedItemList = []
        for _ in range(chosenItemCount):
            selectedItemList.append(self.memoList.GetItem(nextItem, 1).GetText())
            nextItem = self.memoList.GetNextItem(nextItem)

        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject('\n'.join(selectedItemList)))
            wx.TheClipboard.Close()


    def _get_uri_from_data(self, raw_data):
        if len(raw_data) == 0:
            return

        idx = raw_data.find('\n')
        if idx == -1:
            return ""
        return raw_data[:idx]


    def OnUpdateList(self, memoData):
        self.logger.info('.')
        memoList = []

        for k, memo in memoData.items():
            memoList.insert(0, memo)

        self.memoList.DeleteAllItems()

        count = 0
        for memo in memoList:
            count += 1
            if count > self.max_list_count:
                break
            index = self.memoList.InsertItem(self.memoList.GetItemCount(), 1)
            self.memoList.SetItem(index, 0, memo['index'])
            self.memoList.SetItem(index, 1, memo['id'])

            #summary = memo['memo']
            #if len(summary) > 20:
            #    summary = memo['memo'][:20]
            #self.memoList.SetItem(index, 2, summary)
            if index % 2 == 0:
                self.memoList.SetItemBackgroundColour(index, "Light blue")


    def _OnSaveMemo(self, event):
        self.OnSaveMemo()


    def OnSaveMemo(self):
        self.logger.info('.')
        self.parent.OnSaveMemo()


    def set_max_list_count(self, count):
        self.max_list_count = count


    def get_max_list_count(self):
        return self.max_list_count


    def __HasItem(self) -> bool:
        if self.memoList.GetItemCount() == 0:
            self.logger.info("List is empty!")
            return False

        if self.currentItem < 0:
            self.currentItem = 0

        if self.currentItem >= self.memoList.GetItemCount():
            self.currentItem = 0

        return True


    def on_clone_memo(self):
        if not self.__HasItem():
            return

        chosenItem = self.memoList.GetItem(self.currentItem, 0).GetText()
        self.parent.OnCloneMemo(chosenItem)


    def on_toggle_main_search_box(self):
        if self.searchMainText.IsShown():
            self.searchMainText.Hide()
            self.mainSearchClearBtn.Hide()
        else:
            self.searchMainText.Show()
            self.mainSearchClearBtn.Show()
