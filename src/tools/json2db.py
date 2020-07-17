import os
import sys
import json
from manager import dbmanager

def loadJson(filename):
    print("loadJson: " + filename)
    memoList = []
    try:
        if (os.path.isfile(filename)):
            file = open(filename, 'r', encoding="UTF-8")
            lines = file.readlines()
            file.close()

            idx = 0
            for line in lines[1:]:
                memo = json.loads(line)
                idx += 1
                item = {}
                item['id'] = memo["id"]
                item['memo'] = memo["memo"]
                item['index'] = str(idx)
                memoList.append(item)
            print("Success to load " + filename)
        return memoList
    except:
        print("Loading faile:" + filename)

    return []

def save2DB(datas, db_name):
    db = dbmanager.DBManager(db_name)
    print(len(datas))
    #for item in datas:
    #    db.insert([item['id'], item['memo']])
    #db.printDB()

def main(filenames):
    json_file = filenames[0]
    db_file = filenames[1]
    data = loadJson(json_file)
    save2DB(data, db_file)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: json2db json_file db_file")
    else:
        main(sys.argv[1:])