#!/usr/bin/python
#-*- coding: utf-8 -*-

from Observable import Observable
from FileManager import FileManager
from DataManager import DataManager
import logging

UPDATE_MEMO = 1

class MemoManager(Observable):
    def __init__(self):
        self.logger = logging.getLogger("chobomemo")
        self.dataManager = DataManager()
        self.observer = None
        self.fileManager = FileManager()
        self._loadMemo()

    def _loadMemo(self):
        memoData = self.fileManager.loadDataFile()
        self.dataManager.OnSetMemoList(memoData)
        self.OnNotify(UPDATE_MEMO)
   
    def OnCreateMemo(self, memo):
        self.dataManager.OnCreateMemo(memo)
        self.OnNotify(UPDATE_MEMO)

    def OnDeleteMemo(self, memoIdx):
        self.logger.info(memoIdx)
        self.dataManager.OnDeleteMemo(memoIdx)
        self.OnNotify(UPDATE_MEMO)

    def OnGetMemo(self, memoIdx):
        return self.dataManager.OnGetMemo(memoIdx)

    def OnGetMemoList(self):
        return self.dataManager.OnGetMemoList()

    def OnNotify(self, evt):
        if self.observer == None:
            return
        self.observer.OnNotify(evt)

    def OnRegister(self, observer):
        self.observer = observer
        self.OnNotify(UPDATE_MEMO)

    def OnSave(self):
        self.fileManager.saveDataFile(self.OnGetMemoList())

    def OnUpdateMemo(self, memo):
        self.logger.info(memo[2])
        self.dataManager.OnUpdateMemo(memo)
        self.OnNotify(UPDATE_MEMO)

def test():
    '''Test code for TDD'''
    mm = MemoManager()
