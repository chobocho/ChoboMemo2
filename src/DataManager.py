#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging

class DataManager:
    def __init__(self):
        self.logger = logging.getLogger("chobomemo")
        self.memoList = {}
    
    def OnCreateMemo(self, memo):
        nextKey = len(self.memoList) + 1
        self.logger.info(nextKey)
        while (str(nextKey) in self.memoList) == True:
            self.logger.info("Exist " + str(nextKey))
            nextKey += 1
        
        strNextKey = str(nextKey)
        memo.append(strNextKey)
        self.memoList[strNextKey] = memo
        self.logger.info(strNextKey)

    def OnUpdateMemo(self, memo):
        key = memo[2]
        self.memoList[key] = memo
        self.logger.info(key)

    def OnDeleteMemo(self, memoIdx):
        if (memoIdx in self.memoList) == False:
            return 
        del self.memoList[memoIdx]
        #idx = 0
        #for key in self.memoList.keys():
        #    idx += 1
        #    self.memoList[key][2] = str(idx)

    def OnGetMemoList(self):
        return self.memoList

    def OnSetMemoList(self, list):
        self.memoList = list.copy()
        self.logger.info("length of memoList is " + str(len(self.memoList)))

    def OnGetMemo(self, memoIdx):
        return self.memoList[memoIdx]

def test():
    '''Test code for TDD'''
    dm = DataManager()