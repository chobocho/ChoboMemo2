#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging
import textutil
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
        nextKey = len(self.memoListOrigin) + 1
        self.logger.info(nextKey)
        while (str(nextKey) in self.memoListOrigin) == True:
            self.logger.info("Exist " + str(nextKey))
            nextKey += 1
        
        strNextKey = str(nextKey)
        memo['index'] = strNextKey
        self.memoListOrigin[strNextKey] = memo.copy()
        self.hasUpdated = True
        self.logger.info(strNextKey)
        self.memoList = self.memoListOrigin.copy()

    def OnUpdateMemo(self, memo):
        key = memo['index']
        self.memoListOrigin[key] = memo.copy()
        self.hasUpdated = True
        self.logger.info(key)
        self.memoList = self.memoListOrigin.copy()

    def OnDeleteMemo(self, memoIdx):
        if (memoIdx in self.memoListOrigin) == False:
            return 
        del self.memoListOrigin[memoIdx]
        self.hasUpdated = True
        self.memoList = self.memoListOrigin.copy()

    def OnGetFilteredMemoList(self):
        return self.memoList

    def OnGetMemoList(self):
        return self.memoListOrigin

    def OnSetMemoList(self, list):
        self.memoListOrigin = list.copy()
        self.memoList =  list.copy()
        self.logger.info("length of memoList is " + str(len(self.memoList)))

    def OnGetMemo(self, memoIdx, searchKeyword=""):
        memo = self.memoList[memoIdx].copy()
        keywordList = searchKeyword.lower().split('|')
        highLightPosition = textutil.searchKeyword(memo['memo'].lower(), keywordList)
        memo['highlight'] = highLightPosition[:]
        return memo

    def OnSetFilter(self, filter_):
        filter = filter_.strip().lower()
        if len(filter) == 0:
            self.memoList = self.memoListOrigin.copy()
            return

        self.memoList = {}
        for key in self.memoListOrigin.keys():
            if filter in self.memoListOrigin[key]['id'].lower():
                self.memoList[key] = self.memoListOrigin[key]
            elif filter in self.memoListOrigin[key]['memo'].lower():
                self.memoList[key] = self.memoListOrigin[key]

def test():
    '''Test code for TDD'''
    dm = DataManager()