import unittest
import os
import FileManager
import MemoManager
import DataManager
import textutil
import loadfilev1
import loadfilev2


class ChoboMemoTest(unittest.TestCase):
    def test_FileManager(self):
        FileManager.test()

    def test_DataManager(self):
        DataManager.test()

    def test_MemoManager(self):
        MemoManager.test()

    def test_textutil(self):
        textutil.test()

    def test_loadfilev1(self):
        fm = loadfilev1.LoadFile()
        fm.loadfile("")

    def test_loadfilev2(self):
        fm = loadfilev2.LoadFile()
        fm.loadfile("")

if __name__ == '__main__':
    unittest.main()