#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging
import json
import os

from util import compress


class CompressedLoadFile:
    def __init__(self):
        self.logger = logging.getLogger("chobomemo")

    def loadfile(self, filename):
        memoList = {}
        try:
            if os.path.isfile(filename):
                file = open(filename, 'r', encoding="UTF-8")
                lines = file.readlines()
                file.close()

                idx = 0
                for line in lines[1:]:
                    memo = json.loads(line)
                    idx += 1
                    item = {}
                    item['id'] = memo["id"]
                    item['memo'] = compress.decompress(memo["memo"])
                    item['index'] = str(idx)
                    memoList[item['index']] = item
                self.logger.info("Success to load " + filename)
            return memoList
        except:
            self.logger.exception("Loading failed:" + filename)

        return {}


def test():
    """For unittest"""
    fm = LoadFile()
    assert fm.loadfile("") == {}


