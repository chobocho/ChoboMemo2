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
        self.INDEX_COLUMN_WIDTH = 60
        self.logger = logging.getLogger("chobomemo")
        self.parent = parent
        self.max_list_count = 99
        self.cache = memo_cache.MemoCache()
        self.current_item = -1
        self.list_height = list_height
        self._init_ui()
        self.is_resized = False

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
        self.memo_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self._on_update_memo)
        self.memo_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._open_uri)
        self.memo_list.InsertColumn(0, "No", width=self.INDEX_COLUMN_WIDTH)
        self.memo_list.InsertColumn(1, "Title", width=240)
        self.memo_list.SetFont(font)
        self.current_item = -1
        ##
        self._add_memo_btn_box(sizer)
        ##
        self.SetSizer(sizer)
        self.SetSizerAndFit(sizer, True)

        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_IDLE, self.on_idle)

    def _add_memo_btn_box(self, sizer):
        memo_mng_btn_box = wx.BoxSizer(wx.HORIZONTAL)
        self.find_memo_btn = wx.Button(self, wx.NewId(), "Find", size=(55, 30))
        self.find_memo_btn.SetToolTip("Show Find popup (Ctrl+F)")
        self.find_memo_btn.Bind(wx.EVT_BUTTON, self._on_find_memo)
        memo_mng_btn_box.Add(self.find_memo_btn, 1, wx.ALIGN_CENTRE, 1)
        self.editMemoBtn = wx.Button(self, wx.NewId(), "Edit", size=(55, 30))
        self.editMemoBtn.SetToolTip("Show Editor popup (Ctrl+U)")
        self.editMemoBtn.Bind(wx.EVT_BUTTON, self._on_update_memo)
        memo_mng_btn_box.Add(self.editMemoBtn, 1, wx.ALIGN_CENTRE, 1)
        self.createMemoBtn = wx.Button(self, wx.NewId(), "New", size=(55, 30))
        self.createMemoBtn.SetToolTip("Create a new memo (Ctrl+N)")
        self.createMemoBtn.Bind(wx.EVT_BUTTON, self._on_create_memo)
        memo_mng_btn_box.Add(self.createMemoBtn, 1, wx.ALIGN_CENTRE, 1)
        self.memoDeleteBtn = wx.Button(self, wx.NewId(), "Delete", size=(55, 30))
        self.memoDeleteBtn.SetToolTip("Delete a selected memo (Ctrl+Alte+D)")
        self.memoDeleteBtn.Bind(wx.EVT_BUTTON, self._on_delete_memo)
        memo_mng_btn_box.Add(self.memoDeleteBtn, 1, wx.ALIGN_CENTRE, 1)
        self.memoSaveBtn = wx.Button(self, wx.NewId(), "Save", size=(55, 30))
        self.memoSaveBtn.SetToolTip("Save as a CFM (Ctrl+S)")
        self.memoSaveBtn.Bind(wx.EVT_BUTTON, self._on_save_memo)
        self.memoSaveBtn.SetToolTip("Save as CFM file")
        memo_mng_btn_box.Add(self.memoSaveBtn, 1, wx.ALIGN_CENTRE, 1)
        sizer.Add(memo_mng_btn_box, 0, wx.ALIGN_LEFT, 1)

    def _init_main_search_ui(self, sizer):
        main_search_box = wx.BoxSizer(wx.VERTICAL)

        list_mng_btn_box = wx.BoxSizer(wx.HORIZONTAL)

        lbl_space = wx.StaticText(self, wx.NewId(), " ", size=(10, 25))
        list_mng_btn_box.Add(lbl_space, 0, wx.ALIGN_LEFT, 1)
        self.cb_lock_search_text = wx.CheckBox(self, wx.NewId(), size=(20, 25))
        self.cb_lock_search_text.SetToolTip("Ctrl+L: Lock search keyword")
        list_mng_btn_box.Add(self.cb_lock_search_text, 0, wx.ALIGN_LEFT, 1)
        self.searchText = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(170, 25))
        self.searchText.Bind(wx.EVT_TEXT_ENTER, self.OnSearchKeyword)
        self.searchText.SetValue("")
        self.searchText.SetHint("Alt+D: Set focus here!")
        list_mng_btn_box.Add(self.searchText, 0, wx.ALIGN_CENTRE, 1)
        self.searchBtn = wx.Button(self, wx.NewId(), "Find", size=(50, 25))
        self.searchBtn.Bind(wx.EVT_BUTTON, self.OnSearchKeyword)
        list_mng_btn_box.Add(self.searchBtn, 0, wx.ALIGN_CENTRE, 1)
        self.searchClearBtn = wx.Button(self, wx.NewId(), "Clear", size=(50, 25))
        self.searchClearBtn.SetToolTip("Clear search keyword (Alt+C)")
        self.searchClearBtn.Bind(wx.EVT_BUTTON, self.OnSearchClear)
        list_mng_btn_box.Add(self.searchClearBtn, 1, wx.ALIGN_CENTRE, 1)

        main_search_box.Add(list_mng_btn_box, 0, wx.ALIGN_LEFT, 1)
        sizer.Add(main_search_box, 0, wx.ALIGN_LEFT, 1)

    def _on_create_memo(self, event):
        self.parent.save_memo_panel()
        self.on_create_memo()

    def on_create_memo(self):
        new_memo = {'id': '', 'memo': ''}

        dlg = MemoDialog(None, title='Create new memo')
        if dlg.ShowModal() == wx.ID_OK:
            new_memo = {'id': dlg.GetTopic(),
                        'memo': dlg.GetValue()}
            self.parent.on_create_memo(new_memo)
        dlg.Destroy()

        title = new_memo['id']
        self._on_set_search_keyword(title)
        self._on_search_keyword(title)
        self.cache.add(title)

    def _on_find_memo(self, event):
        self.parent.save_memo_panel()
        self.parent.run_advanced_find()

    def _on_update_memo(self, event):
        self.parent.save_memo_panel()
        self.on_update_memo()

    def on_update_memo(self):
        if not self._has_item():
            return

        current_search_keyword = self.searchText.GetValue()

        chosen_item = self.memo_list.GetItem(self.current_item, 0).GetText()
        self.logger.info(f'{str(self.current_item)}:{chosen_item}')
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
        if self.cb_lock_search_text.GetValue():
            self._on_search_keyword(current_search_keyword)
        else:
            self._on_set_search_keyword(title)
            self._OnSearchKeywordInTitle(title)
        self.cache.add(title)

    def _on_delete_memo(self, event):
        self.parent.save_memo_panel()
        self.on_delete_memo()

    def on_delete_memo(self):
        self.logger.info(self.current_item)

        if not self._has_item():
            return

        current_search_keyword = self.searchText.GetValue()
        chosen_item = self.memo_list.GetItem(self.current_item, 0).GetText()
        memo_title = self.memo_list.GetItem(self.current_item, 1).GetText()
        ask_delete_dialog = wx.MessageDialog(None, msg := f'Do you want to delete [{chosen_item}] {memo_title}',
                                             title := 'Delete memo',
                                             wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if ask_delete_dialog.ShowModal() == wx.ID_YES:
            self.parent.OnDeleteMemo(chosen_item)
            self.logger.info(msg)
        ask_delete_dialog.Destroy()

        if self.cb_lock_search_text.GetValue():
            self._on_search_keyword(current_search_keyword)
        else:
            self._on_set_search_keyword(title)
            self._OnSearchKeywordInTitle(title)

    def OnSearchClear(self, event):
        self.parent.save_memo_panel()
        self.on_clear_filter()

    def on_clear_filter(self):
        self.searchText.SetValue("")
        self._on_search_keyword("")

    def on_focus_filter(self):
        self.searchText.SetFocus()

    def OnSearchKeyword(self, event):
        self.parent.save_memo_panel()
        input_search_keyword = self.searchText.GetValue()
        search_keyword = input_search_keyword.strip()
        self._on_search_keyword(search_keyword)

    def on_set_filter_keyword(self, keyword):
        self._on_set_search_keyword(keyword)

    def _on_set_search_keyword(self, keyword):
        self.searchText.SetValue(keyword)

    def _on_search_keyword(self, search_keyword):
        self.parent.OnSearchKeyword(search_keyword)

    def _OnSearchKeywordInTitle(self, search_keyword):
        self.parent.OnSearchKeywordInTitle(search_keyword)

    def _OnItemSelected(self, event):
        if self.current_item != event.Index:
            self.parent.save_memo_panel()
        self.current_item = event.Index
        self.OnItemSelected(self.current_item)

    def OnItemSelected(self, index):
        if self.memo_list.GetItemCount() == 0:
            self.logger.info("List is empty!")
            return
        if index < 0:
            index = 0
        chosen_item = self.memo_list.GetItem(index, 0).GetText()
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

    @staticmethod
    def _get_uri_from_data(raw_data):
        if len(raw_data) == 0:
            return ""

        if (idx := raw_data.find('\n')) == -1:
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
        self.parent.save_memo_panel()
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
        chosen_item_title = self.memo_list.GetItem(self.current_item, 1).GetText()
        self.parent.OnCloneMemo(chosen_item)
        self._OnSearchKeywordInTitle(chosen_item_title)

    def on_toggle_save_btn(self, enable):
        if enable and (self.memoSaveBtn.IsShown() is False):
            self.memoSaveBtn.Show()
        elif (enable is False) and self.memoSaveBtn.IsShown():
            self.memoSaveBtn.Hide()

    def on_toggle_search_lock(self):
        value = self.cb_lock_search_text.GetValue() ^ True
        self.cb_lock_search_text.SetValue(value)

    def on_resize(self, event):
        self.is_resized = True

    def on_idle(self, event):
        if self.is_resized:
            self.memo_list.SetColumnWidth(1, self.GetSize()[0])
            self.Layout()
            self.is_resized = False