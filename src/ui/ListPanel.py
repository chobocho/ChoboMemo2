#!/usr/bin/python
#-*- coding: utf-8 -*-
import wx
import logging
from ui.MemoUI import MemoDialog
from util import webutil
from manager import memo_cache


class ListPanel(wx.Panel):
    def __init__(self, parent, *args, list_height=600, **kw):
        super(ListPanel, self).__init__(*args, **kw)
        self.logger = logging.getLogger("chobomemo")
        self.parent = parent
        self.max_list_count = 99
        self.cache = memo_cache.MemoCache()
        self.current_item = -1
        self.list_height = list_height
        self._init_ui()

    def _init_ui(self):
        self.logger.info('.')
        font = wx.Font(12, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        ##
        self._init_main_search_ui(sizer)
        ## memoListCtrl
        memo_list_id = wx.NewId()
        self.memo_list = wx.ListCtrl(self, memo_list_id,
                                     style=wx.LC_REPORT
                                         | wx.BORDER_NONE
                                         | wx.LC_EDIT_LABELS,
                                     size=(300, self.list_height))
        sizer.Add(self.memo_list, 1, wx.EXPAND)
        self.memo_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self._OnItemSelected)
        self.memo_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self._OnUpdateMemo)
        self.memo_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._open_uri)
        self.memo_list.InsertColumn(0, "No", width=60)
        self.memo_list.InsertColumn(1, "Title", width=240)
        self.memo_list.SetFont(font)
        self.current_item = -1
        ##
        self._add_memo_btn_box(sizer)
        ##
        self.SetSizer(sizer)
        self.SetSizerAndFit(sizer, True)

    def _add_memo_btn_box(self, sizer):
        memo_mng_btn_box = wx.BoxSizer(wx.HORIZONTAL)
        self.find_memo_btn = wx.Button(self, 10, "Find", size=(55, 30))
        self.find_memo_btn.Bind(wx.EVT_BUTTON, self._on_find_memo)
        memo_mng_btn_box.Add(self.find_memo_btn, 1, wx.ALIGN_CENTRE, 1)
        self.editMemoBtn = wx.Button(self, 10, "Edit", size=(55, 30))
        self.editMemoBtn.Bind(wx.EVT_BUTTON, self._OnUpdateMemo)
        memo_mng_btn_box.Add(self.editMemoBtn, 1, wx.ALIGN_CENTRE, 1)
        self.createMemoBtn = wx.Button(self, 10, "New", size=(55, 30))
        self.createMemoBtn.Bind(wx.EVT_BUTTON, self._on_create_memo)
        memo_mng_btn_box.Add(self.createMemoBtn, 1, wx.ALIGN_CENTRE, 1)
        self.memoSaveBtn = wx.Button(self, 10, "Save", size=(55, 30))
        self.memoSaveBtn.Bind(wx.EVT_BUTTON, self._on_save_memo)
        memo_mng_btn_box.Add(self.memoSaveBtn, 1, wx.ALIGN_CENTRE, 1)
        self.memoDeleteBtn = wx.Button(self, 10, "Delete", size=(55, 30))
        self.memoDeleteBtn.Bind(wx.EVT_BUTTON, self._OnDeleteMemo)
        memo_mng_btn_box.Add(self.memoDeleteBtn, 1, wx.ALIGN_CENTRE, 1)
        sizer.Add(memo_mng_btn_box, 0, wx.ALIGN_LEFT, 1)

    def _init_main_search_ui(self, sizer):
        main_search_box = wx.BoxSizer(wx.VERTICAL)

        list_mng_btn_box = wx.BoxSizer(wx.HORIZONTAL)
        self.searchText = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(200, 25))
        self.searchText.Bind(wx.EVT_TEXT_ENTER, self.OnSearchKeyword)
        self.searchText.SetValue("")
        list_mng_btn_box.Add(self.searchText, 0, wx.ALIGN_CENTRE, 1)
        self.searchBtn = wx.Button(self, 10, "Find", size=(50, 25))
        self.searchBtn.Bind(wx.EVT_BUTTON, self.OnSearchKeyword)
        list_mng_btn_box.Add(self.searchBtn, 0, wx.ALIGN_CENTRE, 1)
        self.searchClearBtn = wx.Button(self, 10, "Clear", size=(50, 25))
        self.searchClearBtn.Bind(wx.EVT_BUTTON, self.OnSearchClear)
        list_mng_btn_box.Add(self.searchClearBtn, 1, wx.ALIGN_CENTRE, 1)

        main_search_box.Add(list_mng_btn_box, 0, wx.ALIGN_LEFT, 1)
        sizer.Add(main_search_box, 0, wx.ALIGN_LEFT, 1)

    def _on_create_memo(self, event):
        self.OnCreateMemo()

    def OnCreateMemo(self):
        new_memo = {'id': '', 'memo': ''}

        dlg = MemoDialog(None, title='Create new memo')
        if dlg.ShowModal() == wx.ID_OK:
            new_memo = {'id': dlg.GetTopic(),
                        'memo': dlg.GetValue()}
            self.parent.on_create_memo(new_memo)
        dlg.Destroy()

        title = new_memo['id']
        self._on_set_search_keyword(title)
        self._OnSearchKeyword(title)
        self.cache.add(title)

    def _on_find_memo(self, event):
        self.parent.run_advanced_find()

    def _OnUpdateMemo(self, event):
        self.OnUpdateMemo()

    def OnUpdateMemo(self):
        if not self._has_item():
            return

        chosen_item = self.memo_list.GetItem(self.current_item, 0).GetText()
        self.logger.info(str(self.current_item) + ':' + chosen_item)
        memo = self.parent.OnGetMemoItem(chosen_item)

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
        self.logger.info(self.current_item)

        if not self._has_item():
            return

        chosen_item = self.memo_list.GetItem(self.current_item, 0).GetText()
        title = self.memo_list.GetItem(self.current_item, 1).GetText()
        msg = f'Do you want to delete [{chosen_item}] {title}'
        title = 'Delete memo'
        ask_delete_dialog = wx.MessageDialog(None, msg, title, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if ask_delete_dialog.ShowModal() == wx.ID_YES:
            self.parent.OnDeleteMemo(chosen_item)
            self.logger.info(msg)
        ask_delete_dialog.Destroy()

    def OnSearchClear(self, event):
        self.on_clear_filter()

    def on_clear_filter(self):
        self.searchText.SetValue("")
        self._OnSearchKeyword("")

    def on_focus_filter(self):
        self.searchText.SetFocus()

    def OnSearchKeyword(self, event):
        input_search_keyword = self.searchText.GetValue()
        search_keyword = input_search_keyword.strip()
        self._OnSearchKeyword(search_keyword)

    def on_set_filter_keyword(self, keyword):
        self._on_set_search_keyword(keyword)

    def _on_set_search_keyword(self, keyword):
        self.searchText.SetValue(keyword)

    def _OnSearchKeyword(self, searchKeyword):
        self.parent.OnSearchKeyword(searchKeyword)

    def _OnSearchKeywordInTitle(self, searchKeyword):
        self.parent.OnSearchKeywordInTitle(searchKeyword)

    def _OnItemSelected(self, event):
        self.current_item = event.Index
        self.OnItemSelected(self.current_item)

    def OnItemSelected(self, index):
        if self.memo_list.GetItemCount() == 0:
            self.logger.info("List is empty!")
            return
        if index < 0:
            index = 0
        chosen_item = self.memo_list.GetItem(index, 0).GetText()
        self.logger.info(str(index) + ':' + chosen_item)
        self.parent.OnGetMemo(chosen_item)

    def _open_uri(self, event):
        self.open_uri()

    def open_uri(self):
        if not self._has_item():
            return

        chosen_item = self.memo_list.GetItem(self.current_item, 0).GetText()
        uri = self.memo_list.GetItem(self.current_item, 1).GetText()

        self._on_set_search_keyword(uri)
        self.cache.add(uri)

        if (len(uri) <= 3) or ("http" not in uri.lower()):
            if webutil.is_special_uri(uri):
                webutil.open_uri(uri)
                return

            memo = self.parent.OnGetMemoItem(chosen_item)
            uri = self._get_uri_from_data(memo['memo'])

        if len(uri) > 3:
            webutil.open_uri(uri)

    def on_copy_title(self):
        if not self._has_item():
            return

        chosen_item_count = self.memo_list.GetSelectedItemCount()
        next_item = self.memo_list.GetFirstSelected()

        selected_item_list = []
        for _ in range(chosen_item_count):
            selected_item_list.append(self.memo_list.GetItem(next_item, 1).GetText())
            next_item = self.memo_list.GetNextItem(next_item)

        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject('\n'.join(selected_item_list)))
            wx.TheClipboard.Close()

    def _get_uri_from_data(self, raw_data):
        if len(raw_data) == 0:
            return

        idx = raw_data.find('\n')
        if idx == -1:
            return ""
        return raw_data[:idx]

    def OnUpdateList(self, memo_data):
        self.logger.info('.')
        memo_list = []

        for k, memo in memo_data.items():
            memo_list.insert(0, memo)

        self.memo_list.DeleteAllItems()

        count = 0
        for memo in memo_list:
            count += 1
            if count > self.max_list_count:
                break
            index = self.memo_list.InsertItem(self.memo_list.GetItemCount(), 1)
            self.memo_list.SetItem(index, 0, memo['index'])
            self.memo_list.SetItem(index, 1, memo['id'])

            if index % 2 == 0:
                self.memo_list.SetItemBackgroundColour(index, "Light blue")

    def _on_save_memo(self, event):
        self.OnSaveMemo()

    def OnSaveMemo(self):
        self.logger.info('.')
        self.parent.OnSaveMemo()

    def set_max_list_count(self, count):
        self.max_list_count = count

    def get_max_list_count(self):
        return self.max_list_count

    def _has_item(self) -> bool:
        if self.memo_list.GetItemCount() == 0:
            self.logger.info("List is empty!")
            return False

        if self.current_item < 0:
            self.current_item = 0

        if self.current_item >= self.memo_list.GetItemCount():
            self.current_item = 0

        return True

    def on_clone_memo(self):
        if not self._has_item():
            return

        chosen_item = self.memo_list.GetItem(self.current_item, 0).GetText()
        self.parent.OnCloneMemo(chosen_item)

