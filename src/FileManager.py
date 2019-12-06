#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging
import json
import os
import wx

class FileManager:
    def __init__(self):
        self.logger = logging.getLogger("chobomemo")
        self.saveFileName = ".\\20201105.cfm"
        self.alternativeDataFileName = "d:\\cfm20181105.cfm"

    def loadDataFile(self, fileName=""):
        memoList = {}
        try:
            dataFile = self.saveFileName

            if len(fileName) > 0:
                dataFile = fileName
            if os.path.isfile(dataFile) == False:
                self.logger.warning("File not exist " + dataFile)
                dataFile = self.saveFileName
            if os.path.isfile(dataFile) == False:
                self.logger.warning("File not exist " + dataFile)
                dataFile = self.alternativeDataFileName

            if (os.path.isfile(dataFile)):
                with open(dataFile) as f:
                    jsonData = json.load(f)
                memoList = {}
                idx = 0
                for memo in jsonData["data"]:
                    idx += 1
                    item = []
                    item.append(memo["id"])
                    item.append(memo["memo"])
                    item.append(str(idx))
                    memoList[item[2]] = item
                self.saveFileName = dataFile
            self.logger.info("Success to load " + dataFile)
            return memoList
        except:
            self.logger.exception("Loading faile:" + dataFile)
            return {}
        return {}

    def saveDataFile(self, memoList, fileName=""):
        saveFileName = self.saveFileName

        if len(fileName) > 0:
            saveFileName = fileName
            self.saveFileName = saveFileName
        savedata = {}
        savedata["version"] = "20201105"
        savedata["data"] = []
        for key in memoList.keys():
            memo = memoList[key]
            item = {}
            item["id"] = memo[0]
            item["memo"] = memo[1]
            savedata["data"].append(item)

        with open(saveFileName, 'w') as outfile:
           json.dump(savedata, outfile)

        self.logger.info("Success to save at " + self.saveFileName)
        return True

def test():
    fm = FileManager()
    fm.loadDataFile()
    '''For unittest'''

