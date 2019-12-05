#!/usr/bin/python
#-*- coding: utf-8 -*-

class Observer:
    def __init__(self):
        pass

    def OnNotify(self, event):
        pass

    def OnSetParent(self, parent):
        pass

    def OnGetMemo(self):
        return []