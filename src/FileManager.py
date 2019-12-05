#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging
import json
import os
import wx

class FileManager:
    def __init__(self):
        self.logger = logging.getLogger("chobomemo")
        self.saveFileName = "d:\\cfm20181105.cfm"

    def loadDataFile(self):
        memoList = []
        try:
            if (os.path.isfile(self.saveFileName)):
                with open(self.saveFileName) as f:
                    jsonData = json.load(f)
                memoList = []
                for memo in jsonData["data"]:
                    item = []
                    item.append(memo["id"])
                    item.append(memo["memo"])
                    memoList.append(item)
            self.logger.info("Success to load " + self.saveFileName)
            return memoList
        except:
            self.logger.exception("Loading faile:" + self.saveFileName)
            dlg = wx.MessageDialog(None, 'Exception happened during loading CFM!',
                     'ChoboMemo', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return []
        return []

def test():
    fm = FileManager()
    fm.loadDataFile()
    '''For unittest'''

