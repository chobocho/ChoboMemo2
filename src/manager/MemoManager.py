#!/usr/bin/python
#-*- coding: utf-8 -*-

from manager.Observable import Observable
from manager.FileManager import FileManager
from manager.DataManager import DataManager
from manager.dbmanager import DBManager
import logging
import os


UPDATE_MEMO = 1


class MemoManager(Observable):
    def __init__(self, callback=None, ask_callback=None):
        super().__init__()
        self.logger = logging.getLogger("chobomemo")
        self.dataManager = DataManager()
        self.observer = None
        self.fileManager = FileManager()
        self.dbm = DBManager('20201105.cfm.db')
        self._load_memo(callback, ask_callback)
        self.canChange = True
        self.and_op = ','
        self.or_op = '|'
        self.save_compressed = False
        self.need_to_save_cfm = False

    def is_need_to_save(self):
        return self.need_to_save_cfm

    def _load_memo(self, callback=None, ask_callback=None):
        filename = '20201105.cfm'
        if (len(memo_data := self.dbm.load()) == 0) and os.path.exists(filename) \
                and (ask_callback is not None) and ask_callback():
            memo_data = self.fileManager.loadDataFile(filename)

            gap = int(len(memo_data) / 100)
            tick = 0
            progress = 0

            for data in memo_data:
                # print(memoData[data]['id'])
                self.dbm.insert([memo_data[data]['id'], memo_data[data]['memo']])
                tick += 1
                if tick >= gap:
                    tick = 0
                    if (None != callback) and (progress < 99):
                        progress += 1
                        callback.Update(progress, str(progress) + "% done!")

        self.dataManager.OnSetMemoList(memo_data)
        self.OnNotify(UPDATE_MEMO)

    def set_split_op(self, and_op, or_op):
        self.and_op = and_op
        self.or_op = or_op
        self.dataManager.set_split_op(self.and_op, self.or_op)

    def set_save_mode(self, save_mode:bool, save_cfm:bool):
        self.save_compressed = save_mode
        self.need_to_save_cfm = save_cfm

    def OnLoadFile(self, filename):
        self.canChange = False
        self.dataManager.OnSetMemoList(self.fileManager.loadDataFile(filename))
        self.OnNotify(UPDATE_MEMO)

    def on_load_db(self):
        self.dataManager.OnSetMemoList(self.dbm.load())
        self.OnNotify(UPDATE_MEMO)

    def on_create_memo(self, memo):
        self._on_create_memo(memo)
        self.OnNotify(UPDATE_MEMO)

    def _on_create_memo(self, memo):
        if not self.canChange:
            return
        self.dataManager.on_create_memo(memo, self.dbm)

    def on_delete_memo(self, memo_idx):
        self.logger.info(memo_idx)
        if not self.canChange:
            return
        self.dataManager.OnDeleteMemo(memo_idx, self.dbm)
        self.OnNotify(UPDATE_MEMO)

    def OnUpdateMemo(self, memo):
        if not self.canChange:
            return
        self.logger.info(memo['index'])
        self.dataManager.OnUpdateMemo(memo, self.dbm)
        self.OnNotify(UPDATE_MEMO)

    def OnGetMemo(self, memo_idx, search_keyword =""):
        return self.dataManager.OnGetMemo(self.dbm, memo_idx, search_keyword)

    def OnGetMemoList(self):
        return self.dataManager.OnGetFilteredMemoList()

    def OnNotify(self, evt):
        if self.observer is None:
            return
        self.observer.OnNotify(evt)

    def OnRegister(self, observer):
        self.observer = observer
        self.OnNotify(UPDATE_MEMO)

    def OnSave(self, filter_name="", filename=""):
        if len(filter_name) == 0:
            if not self.dataManager.OnGetNeedToSave():
                self.logger.info("No need to save CFM!")
                return
            if self.fileManager.saveDataFile(self.dataManager.OnGetMemoList(), need_compress=self.save_compressed):
                self.logger.info("Saved CFM!")
                self.dataManager.on_set_need_to_save(False)
        else:
            if len(filename) == 0:
                self.fileManager.saveDataFile(self.OnGetMemoList(), need_compress=self.save_compressed)
            else:
                self.fileManager.saveDataFile(self.OnGetMemoList(), filename, need_compress=self.save_compressed)

    def OnSaveAsMD(self, memo_idx=-1, filename=""):
        if len(filename) == 0:
            return
        memo = self.OnGetMemo(memo_idx)
        self.fileManager.saveAsMarkdown(memo, filename)

    def OnSetFilter(self, searchKeyword):
        self.dataManager.OnSetFilter(searchKeyword)
        self.OnNotify(UPDATE_MEMO)

    def OnSetFilterInTitle(self, searchKeyword):
        self.dataManager.OnSetFilterInTitle(searchKeyword)
        self.OnNotify(UPDATE_MEMO)

    def OnAddItemFromTextFile(self, filename):
        memo = self._on_add_item_from_text_file(filename)
        self.on_create_memo(memo)

    def _on_add_item_from_text_file(self, filename):
        new_memo = {'id': self.fileManager.getFileNameOnly(filename), 'memo': ''}

        if self.fileManager.getFileSize(filename) > (_1MB := 1024 * 1024):
            self.logger.info("It is bigger than 1MB: " + filename)
            return new_memo

        file_data = self.fileManager.OnLoadTextFile(filename)
        new_memo['memo'] = filename + '\n\n' + ''.join(file_data)
        #print(len(filedata), memo)
        return new_memo

    def on_add_item_by_files(self, files):
        allow_file_name = ['.txt', '.py', '.java', '.cpp']

        #file_list = self.fileManager.getFileList(files)
        file_list = files
        
        for filename in file_list:
            is_processed = False
            for name in allow_file_name:
                if name in filename:
                    new_memo = self._on_add_item_from_text_file(filename)
                    self._on_create_memo(new_memo)
                    is_processed = True
                    break

            if not is_processed:
                new_memo = {'id': self.fileManager.getFileNameOnly(filename), 'memo': f'{filename}\n\n---[Memo]---\n'}
                self._on_create_memo(new_memo)

        self.OnNotify(UPDATE_MEMO)

    def OnCloneMemo(self, memo_idx):
        self.on_create_memo(self.OnGetMemo(memo_idx))


def test():
    """Test code for TDD"""
    mm = MemoManager()
