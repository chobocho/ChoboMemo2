#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging
from util import textutil


class DataManager:
    def __init__(self, and_op=',', or_op='|'):
        self.logger = logging.getLogger("chobomemo")
        self.memo_list = {}
        self.memo_list_origin = {}
        self.has_updated = False
        self.enable_db = True
        self.and_op = and_op
        self.or_op = or_op

    def set_split_op(self, and_op, or_op):
       self.and_op = and_op
       self.or_op = or_op

    def on_set_need_to_save(self, flag):
        self.has_updated = flag

    def OnGetNeedToSave(self):
        return self.has_updated

    def on_create_memo(self, memo, dbm):
        memo['index'] = str(dbm.insert([memo['id'], memo['memo']]))
        self.memo_list_origin[memo['index']] = memo.copy()
        self.has_updated = True
        self.logger.info(memo['index'])
        self.memo_list = self.memo_list_origin.copy()

    def OnUpdateMemo(self, memo, dbm):
        key = memo['index']
        dbm.update((memo['id'], memo['memo'], memo['index']))
        self.memo_list_origin[key] = memo.copy()
        self.has_updated = True
        self.logger.info(key)
        self.memo_list = self.memo_list_origin.copy()

    def OnDeleteMemo(self, memo_idx, dbm):
        if not (memo_idx in self.memo_list_origin):
            return
        dbm.delete(memo_idx)
        del self.memo_list_origin[memo_idx]
        self.has_updated = True
        self.memo_list = self.memo_list_origin.copy()

    def OnGetFilteredMemoList(self):
        return self.memo_list

    def OnGetMemoList(self):
        return self.memo_list_origin

    def OnSetMemoList(self, list):
        self.memo_list_origin = list.copy()
        self.memo_list =  list.copy()
        self.logger.info("length of memoList is " + str(len(self.memo_list)))

    def OnGetMemo(self, dbm, memoIdx, searchKeyword=""):
        if len(self.memo_list) == 0:
            return self.__get_emptyMemo(memoIdx)

        if len(memoIdx) == 0:
            return self.__get_emptyMemo(memoIdx)

        if len(self.memo_list.get(memoIdx, "")) == 0:
            return self.__get_emptyMemo(memoIdx)

        memo_from_db = dbm.read(memoIdx)
        if len(memo_from_db) == 0:
            self.OnDeleteMemo(memoIdx, dbm)
            memo = self.__get_emptyMemo(memoIdx)
            memo['memo'] = "\n It is removed memo.\n\n Please press Clear button."
            return memo
        else:
            self.memo_list[memoIdx]['title'] = memo_from_db['title']
            self.memo_list[memoIdx]['memo'] = memo_from_db['memo']
            self.logger.info("DB updated: " + memoIdx)
        memo = self.memo_list[memoIdx].copy()
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
            self.memo_list = self.memo_list_origin.copy()
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
            self.memo_list = self.memo_list_origin.copy()
            return
        self.__OnFindSimpleKeywordInTitle(filter_keyword)

    def __OnFindSimpleKeywordInTitle(self, filter_keyword):
        self.memo_list = {}

        filter_list = filter_keyword.split('|')

        for key in self.memo_list_origin.keys():
            for searchKey in filter_list:
                if searchKey.lower() in self.memo_list_origin[key]['id'].lower():
                    self.memo_list[key] = self.memo_list_origin[key]
                    break

    def __OnFindSimpleKeyword(self, filter_keyword):
        if filter_keyword[0] == '!' or filter_keyword[0] == '~':
            self._FindHasNotFilterList(filter_keyword[1:])
        else:
            self._FindHasFilterList(filter_keyword)


    def _FindHasFilterList(self, filter_keyword):
        self.memo_list = {}
        for key in self.memo_list_origin.keys():
            if filter_keyword in self.memo_list_origin[key]['id'].lower():
                self.memo_list[key] = self.memo_list_origin[key]
            elif filter_keyword in self.memo_list_origin[key]['memo'].lower():
                self.memo_list[key] = self.memo_list_origin[key]


    def _FindHasNotFilterList(self, filter_keyword):
        self.memo_list = {}
        for key in self.memo_list_origin.keys():
            hasKeyword = False

            if filter_keyword in self.memo_list_origin[key]['id'].lower():
                hasKeyword = True
            if filter_keyword in self.memo_list_origin[key]['memo'].lower():
                hasKeyword = True

            if not hasKeyword:
                self.memo_list[key] = self.memo_list_origin[key]


    def __OnFindOrKeywordList(self, filter_keyword):
        self.memo_list = {}

        if len(filter_keyword) == 0:
            return

        for key in self.memo_list_origin.keys():
            for filter in filter_keyword:
                if filter in self.memo_list_origin[key]['id'].lower():
                    self.memo_list[key] = self.memo_list_origin[key]
                    break
                elif filter in self.memo_list_origin[key]['memo'].lower():
                    self.memo_list[key] = self.memo_list_origin[key]
                    break


    def __OnFindAndKeywordList(self, filter_keyword):
        self.memo_list = {}

        if len(filter_keyword) == 0:
            return

        for key in self.memo_list_origin.keys():
            is_find = False

            for filter in filter_keyword:
                if filter[0] == '!' or filter[0] == '~':
                    keyword = filter[1:]
                    is_find = True

                    if keyword in self.memo_list_origin[key]['id'].lower():
                        is_find = False
                    if keyword in self.memo_list_origin[key]['memo'].lower():
                        is_find = False

                else:
                    is_find = False

                    if filter in self.memo_list_origin[key]['id'].lower():
                        is_find = True
                    elif filter in self.memo_list_origin[key]['memo'].lower():
                        is_find = True

                if not is_find:
                   break

            if is_find:
                self.memo_list[key] = self.memo_list_origin[key]


def test():
    """Test code for TDD"""
    dm = DataManager()