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
        self._loadMemo(callback, ask_callback)
        self.canChange = True
        self.and_op = ','
        self.or_op = '|'
        self.save_compressed = False
        self.need_to_save_cfm = False

    def is_need_to_save(self):
        return self.need_to_save_cfm

    def _loadMemo(self, callback=None, ask_callback=None):
        memoData = self.dbm.load()
        filename = '20201105.cfm'
        if (len(memoData) == 0) and os.path.exists(filename) and (ask_callback is not None) and ask_callback():
            memoData = self.fileManager.loadDataFile(filename)

            gap = int(len(memoData) / 100)
            tick = 0
            progress = 0

            for data in memoData:
                # print(memoData[data]['id'])
                self.dbm.insert([memoData[data]['id'], memoData[data]['memo']])
                tick += 1
                if tick >= gap:
                    tick = 0
                    if (None != callback) and (progress < 99):
                        progress += 1
                        callback.Update(progress, str(progress) + "% done!")

        self.dataManager.OnSetMemoList(memoData)
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
        memoData = self.fileManager.loadDataFile(filename)
        self.dataManager.OnSetMemoList(memoData)
        self.OnNotify(UPDATE_MEMO)

    def OnLoadDB(self):
        memoData = self.dbm.load()
        self.dataManager.OnSetMemoList(memoData)
        self.OnNotify(UPDATE_MEMO)

    def on_create_memo(self, memo):
        self._on_create_memo(memo)
        self.OnNotify(UPDATE_MEMO)

    def _on_create_memo(self, memo):
        if not self.canChange:
            return
        self.dataManager.on_create_memo(memo, self.dbm)

    def OnDeleteMemo(self, memoIdx):
        self.logger.info(memoIdx)
        if not self.canChange:
            return
        self.dataManager.OnDeleteMemo(memoIdx, self.dbm)
        self.OnNotify(UPDATE_MEMO)

    def OnUpdateMemo(self, memo):
        if not self.canChange:
            return
        self.logger.info(memo['index'])
        self.dataManager.OnUpdateMemo(memo, self.dbm)
        self.OnNotify(UPDATE_MEMO)

    def OnGetMemo(self, memoIdx, searchKeyword = ""):
        return self.dataManager.OnGetMemo(self.dbm, memoIdx, searchKeyword)

    def OnGetMemoList(self):
        return self.dataManager.OnGetFilteredMemoList()

    def OnNotify(self, evt):
        if self.observer is None:
            return
        self.observer.OnNotify(evt)

    def OnRegister(self, observer):
        self.observer = observer
        self.OnNotify(UPDATE_MEMO)

    def OnSave(self, filter="", filename=""):
        if len(filter) == 0:
            if not self.dataManager.OnGetNeedToSave():
                self.logger.info("No need to save CFM!")
                return
            if self.fileManager.saveDataFile(self.dataManager.OnGetMemoList(), needCompress=self.save_compressed):
                self.logger.info("Saved CFM!")
                self.dataManager.on_set_need_to_save(False)
        else:
            if len(filename) == 0:
                self.fileManager.saveDataFile(self.OnGetMemoList(), needCompress=self.save_compressed)
            else:
                self.fileManager.saveDataFile(self.OnGetMemoList(), filename, needCompress=self.save_compressed)

    def OnSaveAsMD(self, memoIdx=-1, filename=""):
        if len(filename) == 0:
            return
        memo = self.OnGetMemo(memoIdx)
        self.fileManager.saveAsMarkdown(memo, filename)

    def OnSetFilter(self, searchKeyword):
        self.dataManager.OnSetFilter(searchKeyword)
        self.OnNotify(UPDATE_MEMO)

    def OnSetFilterInTitle(self, searchKeyword):
        self.dataManager.OnSetFilterInTitle(searchKeyword)
        self.OnNotify(UPDATE_MEMO)

    def OnAddItemFromTextFile(self, filename):
        memo = self.__OnAddItemFromTextFile(filename)
        self.on_create_memo(memo)

    def __OnAddItemFromTextFile(self, filename):
        _1MB = 1024 * 1024
        memo = {}
        memo['id'] = self.fileManager.getFileNameOnly(filename)
        memo['memo'] = ''

        if self.fileManager.getFileSize(filename) > _1MB:
            self.logger.info("It is bigger than 1MB: " + filename)
            return memo

        file_data = self.fileManager.OnLoadTextFile(filename)
        memo['memo'] = filename + '\n\n' + ''.join(file_data)
        #print(len(filedata), memo)
        return memo

    def OnAddItemByFiles(self, files):
        allow_file_name = ['.txt', '.py', '.java', '.cpp']

        #file_list = self.fileManager.getFileList(files)
        file_list = files
        
        for filename in file_list:
            is_processed = False
            for name in allow_file_name:
                if name in filename:
                    memo = self.__OnAddItemFromTextFile(filename)
                    self._on_create_memo(memo)
                    is_processed = True
                    break

            if not is_processed:
                memo = {}
                memo['id'] = self.fileManager.getFileNameOnly(filename)
                memo['memo'] = filename + "\n\n---[Memo]---\n"
                self._on_create_memo(memo)

        self.OnNotify(UPDATE_MEMO)


    def OnCloneMemo(self, memoIdx):
        memo = self.OnGetMemo(memoIdx)
        self.on_create_memo(memo)

def test():
    """Test code for TDD"""
    mm = MemoManager()
