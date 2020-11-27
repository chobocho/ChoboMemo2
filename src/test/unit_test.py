import unittest
from manager import DataManager, FileManager, MemoManager
from util import textutil
from store import loadfilev1, loadfilev2
from manager import memo_cache


class ChoboMemoTest(unittest.TestCase):

    def test_memo_cache(self):
        lru = memo_cache.MemoCache()
        lru.add("Hi")
        lru.add("Hello")
        lru.add("Hi")
        self.assertEqual(lru.get_values()[0], 'Hello')
        self.assertEqual(lru.query(), 'Hello|Hi')

if __name__ == '__main__':
    unittest.main()