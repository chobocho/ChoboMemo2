#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging
import json
import os

class SaveFile:
    def __init__(self):
        self.logger = logging.getLogger("chobomemo")

    def savefile(self, memoList, fileName="untile.cfm"):
        savedata = []
        for key in memoList.keys():
            memo = memoList[key]
            item = {}
            item["id"] = memo['id']
            item["memo"] = memo['memo']
            itemString = json.dumps(item)
            savedata.append(itemString)

        version = "version:1105.1"
        with open(fileName, 'w') as outfile:
           outfile.write(version)
           for item in savedata:
               outfile.write('\n')
               outfile.write(item)

        self.logger.info("Success to save at " + fileName)
        return True

def test():
    fm = SaveFile()
    fm.savefile()
    '''For unittest'''

