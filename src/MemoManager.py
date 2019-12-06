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
        if self.observer != None:
            self.observer.OnNotify(UPDATE_MEMO)
   
    def OnDeleteMemo(self, memoIdx):
        pass

    def OnGetMemo(self, memoIdx):
        return self.dataManager.OnGetMemo(memoIdx)

    def OnGetMemoList(self):
        return self.dataManager.OnGetMemoList()

    def OnRegister(self, observer):
        self.observer = observer
        if self.observer != None:
            self.observer.OnNotify(UPDATE_MEMO)

    def OnSave(self):
        self.fileManager.saveDataFile(self.OnGetMemoList())

def test():
    '''Test code for TDD'''
    mm = MemoManager()
