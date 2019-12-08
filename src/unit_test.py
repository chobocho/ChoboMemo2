import unittest
import os
import FileManager
import MemoManager
import DataManager
import textutil

class ChoboMemoTest(unittest.TestCase):
    def test_FileManager(self):
        FileManager.test()

    def test_DataManager(self):
        DataManager.test()

    def test_MemoManager(self):
        MemoManager.test()

    def test_textutil(self):
        textutil.test()

if __name__ == '__main__':
    unittest.main()