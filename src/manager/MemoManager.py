#!/usr/bin/python
#-*- coding: utf-8 -*-

from manager.Observable import Observable
from manager.FileManager import FileManager
from manager.DataManager import DataManager
from manager.dbmanager import DBManager
import logging

UPDATE_MEMO = 1

class MemoManager(Observable):
    def __init__(self):
        self.logger = logging.getLogger("chobomemo")
        self.dataManager = DataManager()
        self.observer = None
        self.fileManager = FileManager()
        self.dbm = DBManager('20201105.cfm.db')
        self._loadMemo()
        self.canChange = True

    def _loadMemo(self):
        memoData = self.dbm.load()
        self.dataManager.OnSetMemoList(memoData)
        self.OnNotify(UPDATE_MEMO)

    def OnLoadFile(self, filename):
        self.canChange = False
        memoData = self.fileManager.loadDataFile(filename)
        self.dataManager.OnSetMemoList(memoData)
        self.OnNotify(UPDATE_MEMO)

    def OnLoadDB(self):
        memoData = self.dbm.load()
        self.dataManager.OnSetMemoList(memoData)
        self.OnNotify(UPDATE_MEMO)

    def OnCreateMemo(self, memo):
        self.__OnCreateMemo(memo)
        self.OnNotify(UPDATE_MEMO)

    def __OnCreateMemo(self, memo):
        if not self.canChange:
            return
        self.dataManager.OnCreateMemo(memo, self.dbm)

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
        return self.dataManager.OnGetMemo(memoIdx, searchKeyword)

    def OnGetMemoList(self):
        return self.dataManager.OnGetFilteredMemoList()

    def OnNotify(self, evt):
        if self.observer == None:
            return
        self.observer.OnNotify(evt)

    def OnRegister(self, observer):
        self.observer = observer
        self.OnNotify(UPDATE_MEMO)

    def OnSave(self, filter="", filename=""):
        if len(filter) == 0:
            if self.dataManager.OnGetNeedToSave() == False:
                self.logger.info("No need to save!")
                return
            if self.fileManager.saveDataFile(self.dataManager.OnGetMemoList()):
                self.dataManager.OnSetNeedToSave(False)
        else:
            if len(filename) == 0:
                self.fileManager.saveDataFile(self.OnGetMemoList())
            else:
                self.fileManager.saveDataFile(self.OnGetMemoList(), filename)

    def OnSaveAsMD(self, memoIdx=-1, filename=""):
        if len(filename) == 0:
            return
        memo = self.OnGetMemo(memoIdx)
        self.fileManager.saveAsMarkdown(memo, filename)

    def OnSetFilter(self, searchKeyword):
        self.dataManager.OnSetFilter(searchKeyword)
        self.OnNotify(UPDATE_MEMO)

    def OnAddItemFromTextFile(self, filename):
        memo = self.__OnAddItemFromTextFile(filename)
        self.OnCreateMemo(memo)

    def __OnAddItemFromTextFile(self, filename):
        _1MB = 1024 * 1024
        memo = {}
        memo['id'] = self.fileManager.getFileNameOnly(filename)
        memo['memo'] = ''

        if self.fileManager.getFileSize(filename) > _1MB:
            self.logger.info("It is bigger than 1MB: " + filename)
            return memo

        filedata = self.fileManager.OnLoadTextFile(filename)
        memo['memo'] = ''.join(filedata)
        #print(len(filedata), memo)
        return memo

    def OnAddItemByFiles(self, files):
        allow_file_name = ['.txt', '.py', '.java', '.cpp']

        file_list = self.fileManager.getFileList(files)
        for filename in file_list:
            is_processed = False
            for name in allow_file_name:
                if (name in filename):
                    memo = self.__OnAddItemFromTextFile(filename)
                    self.__OnCreateMemo(memo)
                    is_processed = True
                    break

            if not is_processed:
                memo = {}
                memo['id'] = self.fileManager.getFileNameOnly(filename)
                memo['memo'] = ""
                self.__OnCreateMemo(memo)

        self.OnNotify(UPDATE_MEMO)

def test():
    '''Test code for TDD'''
    mm = MemoManager()
