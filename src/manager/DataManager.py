#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging
from util import textutil


class DataManager:
    def __init__(self, and_op=',', or_op='|'):
        self.logger = logging.getLogger("chobomemo")
        self.memoList = {}
        self.memoListOrigin = {}
        self.hasUpdated = False
        self.enableDB = True
        self.and_op = and_op
        self.or_op = or_op

    def set_split_op(self, and_op, or_op):
       self.and_op = and_op
       self.or_op = or_op

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
        if not (memoIdx in self.memoListOrigin):
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

    def OnGetMemo(self, dbm, memoIdx, searchKeyword=""):
        if len(self.memoList) == 0:
            return self.__get_emptyMemo(memoIdx)

        if len(memoIdx) == 0:
            return self.__get_emptyMemo(memoIdx)

        if len(self.memoList.get(memoIdx, "")) == 0:
            return self.__get_emptyMemo(memoIdx)

        memo_from_db = dbm.read(memoIdx)
        if len(memo_from_db) == 0:
            self.OnDeleteMemo(memoIdx, dbm)
            memo = self.__get_emptyMemo(memoIdx)
            memo['memo'] = "\n It is removed memo.\n\n Please press Clear button."
            return memo
        else:
            self.memoList[memoIdx]['title'] = memo_from_db['title']
            self.memoList[memoIdx]['memo'] = memo_from_db['memo']
            self.logger.info("DB updated: " + memoIdx)
        memo = self.memoList[memoIdx].copy()
        keywordList = searchKeyword.lower().split('|')
        highLightPosition = textutil.searchKeyword(memo['memo'].lower(), keywordList)
        memo['highlight'] = highLightPosition[:]
        return memo

    def __get_emptyMemo(self, memoIdx):
        emptyMemo = {}
        emptyMemo['id'] = ""
        emptyMemo['memo'] = ""
        emptyMemo['index'] = str(memoIdx)
        emptyMemo['highlight'] = []
        return emptyMemo

    def OnSetFilter(self, filter_keyword):
        filter_keyword = filter_keyword.strip().lower()
        if len(filter_keyword) == 0:
            self.memoList = self.memoListOrigin.copy()
            return
        if self.or_op in filter_keyword:
            split_filter = filter_keyword.split(self.or_op)
            or_filter = [ key for key in split_filter if len(key.strip()) > 0 ]
            #print(or_filter)
            self.__OnFindOrKeywordList(or_filter)
        elif self.and_op in filter_keyword:
            split_filter = filter_keyword.split(self.and_op)
            and_filter = [ key for key in split_filter if len(key.strip()) > 0 ]
            print(and_filter)
            self.__OnFindAndKeywordList(and_filter)
        else:
            self.__OnFindSimpleKeyword(filter_keyword)

    def OnSetFilterInTitle(self, filter_keyword):
        filter_keyword = filter_keyword.strip().lower()
        if len(filter_keyword) == 0:
            self.memoList = self.memoListOrigin.copy()
            return
        self.__OnFindSimpleKeywordInTitle(filter_keyword)

    def __OnFindSimpleKeywordInTitle(self, filter_keyword):
        self.memoList = {}

        filter_list = filter_keyword.split('|')

        for key in self.memoListOrigin.keys():
            for searchKey in filter_list:
                if searchKey.lower() in self.memoListOrigin[key]['id'].lower():
                    self.memoList[key] = self.memoListOrigin[key]
                    break

    def __OnFindSimpleKeyword(self, filter_keyword):
        if filter_keyword[0] == '!' or filter_keyword[0] == '~':
            self._FindHasNotFilterList(filter_keyword[1:])
        else:
            self._FindHasFilterList(filter_keyword)


    def _FindHasFilterList(self, filter_keyword):
        self.memoList = {}
        for key in self.memoListOrigin.keys():
            if filter_keyword in self.memoListOrigin[key]['id'].lower():
                self.memoList[key] = self.memoListOrigin[key]
            elif filter_keyword in self.memoListOrigin[key]['memo'].lower():
                self.memoList[key] = self.memoListOrigin[key]


    def _FindHasNotFilterList(self, filter_keyword):
        self.memoList = {}
        for key in self.memoListOrigin.keys():
            hasKeyword = False

            if filter_keyword in self.memoListOrigin[key]['id'].lower():
                hasKeyword = True
            if filter_keyword in self.memoListOrigin[key]['memo'].lower():
                hasKeyword = True

            if not hasKeyword:
                self.memoList[key] = self.memoListOrigin[key]


    def __OnFindOrKeywordList(self, filter_keyword):
        self.memoList = {}

        if len(filter_keyword) == 0:
            return

        for key in self.memoListOrigin.keys():
            for filter in filter_keyword:
                if filter in self.memoListOrigin[key]['id'].lower():
                    self.memoList[key] = self.memoListOrigin[key]
                    break
                elif filter in self.memoListOrigin[key]['memo'].lower():
                    self.memoList[key] = self.memoListOrigin[key]
                    break


    def __OnFindAndKeywordList(self, filter_keyword):
        self.memoList = {}

        if len(filter_keyword) == 0:
            return

        for key in self.memoListOrigin.keys():
            is_find = False

            for filter in filter_keyword:
                if filter[0] == '!' or filter[0] == '~':
                    keyword = filter[1:]
                    is_find = True

                    if keyword in self.memoListOrigin[key]['id'].lower():
                        is_find = False
                    if keyword in self.memoListOrigin[key]['memo'].lower():
                        is_find = False

                else:
                    is_find = False

                    if filter in self.memoListOrigin[key]['id'].lower():
                        is_find = True
                    elif filter in self.memoListOrigin[key]['memo'].lower():
                        is_find = True

                if not is_find:
                   break

            if is_find:
                self.memoList[key] = self.memoListOrigin[key]


def test():
    """Test code for TDD"""
    dm = DataManager()