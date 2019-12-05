#!/usr/bin/python
#-*- coding: utf-8 -*-

from Observer import Observer
from FileManager import FileManager
from DataManager import DataManager
import logging

class MemoManager(Observer):
    def __init__(self, parent = None):
        self.logger = logging.getLogger("chobomemo")
        self.parent = parent
        self.dataManager = DataManager()
        self._loadMemo()

    def _loadMemo(self):
        fm = FileManager()
        memoData = fm.loadDataFile()
        self.dataManager.setMemoList(memoData)
        if self.parent != None:
            self.parent.OnUpdateMemoList(self.dataManager.getMemoList())

    def OnSetParent(self, parent):
        self.parent = parent
        if self.parent != None:
            self.parent.OnUpdateMemoList(self.dataManager.getMemoList())

    def OnGetMemo(self, memoIdx):
        return self.dataManager.OnGetMemo(memoIdx)

def test():
    '''Test code for TDD'''
    mm = MemoManager()
