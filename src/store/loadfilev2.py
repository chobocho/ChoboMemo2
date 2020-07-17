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
            if (os.path.isfile(filename)):
                file = open(filename, 'r', encoding="UTF-8")
                lines = file.readlines()
                file.close()

                idx = 0
                for line in lines[1:]:
                    memo = json.loads(line)
                    idx += 1
                    item = {}
                    item['id'] = memo["id"]
                    item['memo'] = memo["memo"]
                    item['index'] = str(idx)
                    memoList[item['index']] = item
                self.logger.info("Success to load " + filename)
            return memoList
        except:
            self.logger.exception("Loading faile:" + filename)
            return {}
        return {}

def test():
    '''For unittest'''
    fm = LoadFile()
    assert fm.loadfile("") == {}


