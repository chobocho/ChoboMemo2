#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging
import json
import os

class LoadFile:
    def __init__(self):
        self.logger = logging.getLogger("chobomemo")

    def loadfile(self, filename):
        memoList = {}
        try:
            if os.path.isfile(filename):
                with open(filename) as f:
                    jsonData = json.load(f)
                memoList = {}
                idx = 0
                for memo in jsonData["data"]:
                    idx += 1
                    item = {}
                    item['id'] = memo["id"]
                    item['memo'] = memo["memo"]
                    item['index'] = str(idx)
                    memoList[item['index']] = item
                self.logger.info("Success to load " + filename)
            return memoList
        except:
            self.logger.exception("Loading failed:" + filename)
            return {}
        return {}


def test():
    '''For unittest'''
    fm = LoadFile()
    assert fm.loadfile("") == {}
    fm.loadfile("v1_test05.cfm")


