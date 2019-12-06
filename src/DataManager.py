#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging

class DataManager:
    def __init__(self):
        self.logger = logging.getLogger("chobomemo")
        self.memoList = []
    
    def OnGetMemoList(self):
        return self.memoList;

    def OnSetMemoList(self, list):
        self.memoList = list[:]
        self.logger.info("length of memoList is " + str(len(self.memoList)))

    def OnGetMemo(self, memoIdx):
        return self.memoList[memoIdx][1]

def test():
    '''Test code for TDD'''
    dm = DataManager()