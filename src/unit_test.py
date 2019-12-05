import unittest
import os
import FileManager
import MemoManager
import DataManager

class ChoboMemoTest(unittest.TestCase):
    def test_FileManager(self):
        FileManager.test()

    def test_DataManager(self):
        DataManager.test()

    def test_MemoManager(self):
        MemoManager.test()

if __name__ == '__main__':
    unittest.main()