#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging

class DataManager:
    def __init__(self):
        self.logger = logging.getLogger("chobomemo")
        self.memoList = {}
        self.memoListOrigin = {}
        self.hasUpdated = False
    
    def OnSetNeedToSave(self, flag):
        self.hasUpdated = flag

    def OnGetNeedToSave(self):
        return self.hasUpdated

    def OnCreateMemo(self, memo):
        nextKey = len(self.memoList) + 1
        self.logger.info(nextKey)
        while (str(nextKey) in self.memoList) == True:
            self.logger.info("Exist " + str(nextKey))
            nextKey += 1
        
        strNextKey = str(nextKey)
        memo.append(strNextKey)
        self.memoList[strNextKey] = memo
        self.hasUpdated = True
        self.logger.info(strNextKey)

    def OnUpdateMemo(self, memo):
        key = memo[2]
        self.memoList[key] = memo
        self.hasUpdated = True
        self.logger.info(key)

    def OnDeleteMemo(self, memoIdx):
        if (memoIdx in self.memoListOrigin) == False:
            return 
        del self.memoListOrigin[memoIdx]
        self.hasUpdated = True

        if (memoIdx in self.memoList) == False:
            return 
        del self.memoList[memoIdx]
   

    def OnGetFilteredMemoList(self):
        return self.memoList

    def OnGetMemoList(self):
        return self.memoListOrigin

    def OnSetMemoList(self, list):
        self.memoListOrigin = list.copy()
        self.memoList =  list.copy()
        self.logger.info("length of memoList is " + str(len(self.memoList)))

    def OnGetMemo(self, memoIdx):
        return self.memoList[memoIdx]

    def OnSetFilter(self, filter_):
        filter = filter_.strip().lower()
        if len(filter) == 0:
            self.memoList = self.memoListOrigin.copy()
            return

        self.memoList = {}
        for key in self.memoListOrigin.keys():
            if filter in self.memoListOrigin[key][0].lower():
                self.memoList[key] = self.memoListOrigin[key]
            elif filter in self.memoListOrigin[key][1].lower():
                self.memoList[key] = self.memoListOrigin[key]

def test():
    '''Test code for TDD'''
    dm = DataManager()