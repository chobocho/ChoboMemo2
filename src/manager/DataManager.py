#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging
from util import textutil


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

    def OnCreateMemo(self, memo, dbm):
        memo['index'] = str(dbm.insert([memo['id'], memo['memo']]))
        self.memoListOrigin[memo['index']] = memo.copy()
        self.hasUpdated = True
        self.logger.info(memo['index'])
        self.memoList = self.memoListOrigin.copy()

    def OnUpdateMemo(self, memo, dbm):
        key = memo['index']
        dbm.update((memo['id'], memo['memo'], memo['index']))
        self.memoListOrigin[key] = memo.copy()
        self.hasUpdated = True
        self.logger.info(key)
        self.memoList = self.memoListOrigin.copy()

    def OnDeleteMemo(self, memoIdx, dbm):
        if (memoIdx in self.memoListOrigin) == False:
            return
        dbm.delete(memoIdx)
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
        if len(self.memoList) == 0:
            emptyMemo = {}
            emptyMemo['id'] = ""
            emptyMemo['memo'] = ""
            emptyMemo['index'] = str(memoIdx)
            emptyMemo['highlight'] = []
            return emptyMemo
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