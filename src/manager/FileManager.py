#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging
import os
from store import loadfilev1, loadfilev2, savefilev2


class FileManager:
    def __init__(self):
        self.logger = logging.getLogger("chobomemo")
        self.saveFileName = ".\\20201105.cfm"
        self.alternativeDataFileName = "d:\\cfm20181105.cfm"

    def loadDataFile(self, fileName=""):
        dataFile = self.saveFileName

        if len(fileName) > 0:
            self.logger.info(fileName)
            dataFile = fileName
        if os.path.isfile(dataFile) == False:
            self.logger.warning("File not exist " + dataFile)
            dataFile = self.saveFileName
        if os.path.isfile(dataFile) == False:
            self.logger.warning("File not exist " + dataFile)
            dataFile = self.alternativeDataFileName

        if (os.path.isfile(dataFile)) == False:
            return {}

        version = ""
        try:
            file = open(dataFile, 'rt', encoding="UTF-8")
            version = file.readline()
            file.close()
        except:
            self.logger.exception("File to load " + dataFile)
            return {}

        self.saveFileName = dataFile
        fm = None

        if version.strip() == "version:1105.1":
             fm = loadfilev2.LoadFile()
        else:
             fm = loadfilev1.LoadFile()
        return fm.loadfile(dataFile)


    def saveDataFile(self, memoList, fileName=""):
        saveFileName = self.saveFileName

        if len(fileName) > 0:
            saveFileName = fileName
            self.saveFileName = saveFileName

        fm = savefilev2.SaveFile()
        fm.savefile(memoList, saveFileName)

        self.logger.info("Success to save at " + self.saveFileName)
        return True

    def saveAsMarkdown(self, memo, filename):
        with open(filename, 'w') as outfile:
            outfile.write('# '+ memo['id'] + '  \n\n')
            outfile.write('```\n' + memo['memo'] + '\n```')

def test():
    fm = FileManager()
    fm.loadDataFile()
    '''For unittest'''

