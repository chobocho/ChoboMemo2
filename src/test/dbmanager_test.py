import unittest
from manager import dbmanager

class DBManagerCase(unittest.TestCase):
    def test_createDB(self):
        db_name = "./test.db"
        dbm = dbmanager.DBManager(db_name)

if __name__ == '__main__':
    unittest.main()
