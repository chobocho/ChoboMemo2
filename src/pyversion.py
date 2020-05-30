import os
import json
import traceback
import copy
import datetime

class VersionInfo():
    def __init__(self):
        self.versionDataFile = "version.json"
        self.versionInfo = {}
        self.initVersionInfo()

    def getVersionInfo(self):
        result = copy.deepcopy(self.versionInfo)
        return result

    def updateVersionInfo(self, filename = ""):
        if len(filename) > 1:
            self.versionDataFile = filename
        self._readVersionInfo()
        self._makeVersionInfoFile(self._makeNewVersion(), self.versionInfo['filename'])
        self._saveVersionInfo()
        
    def _makeVersionInfoFile(self, data, filename):
        f = open(filename, 'w', encoding="UTF-8")
        f.write(data)
        f.close()
        
    def _makeNewVersion(self):
        separator = self.versionInfo['separator']
               
        today = datetime.datetime.now()
        yearMonth = chr(65 + today.year - 2001) + chr(65 + today.month - 1)

        if (self.versionInfo['date'] != yearMonth):
            self.versionInfo['month_release_count'] = 1
            self.versionInfo['date'] = yearMonth
            
        new_version = self.versionInfo['header'] + separator
        hexTable="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        new_version += yearMonth + hexTable[int(self.versionInfo['month_release_count'])]
        new_version += self.versionInfo['tail']
        
        return new_version
        
    def _readVersionInfo(self):
        if (os.path.isfile(self.versionDataFile)):
            if self._readJsonFile() == False:
                self._makeVersionFile()
        else:
            self._makeVersionFile()
        
    def _saveVersionInfo(self):  
        #print("_saveVersionInfo")
        jsonData = {}
        jsonData['filename'] = self.versionInfo['filename']
        jsonData['separator'] = self.versionInfo['separator']   
        jsonData['header'] = self.versionInfo['header']
        jsonData['date'] = self.versionInfo['date']
        jsonData['month_release_count'] = self.versionInfo['month_release_count']
        jsonData['tail'] = self.versionInfo['tail']

        aBakFile = open(self.versionDataFile + ".bak" ,'w', encoding="UTF-8")
        aBakFile.write(json.dumps(jsonData))
        aBakFile.close()
      
        f = open(self.versionDataFile,'w', encoding="UTF-8")
        jsonData['month_release_count'] += 1 
        f.write(json.dumps(jsonData))
        f.close()
      
      
    def _readJsonFile(self):
        #print (self.versionDataFile)
        try:
            with open(self.versionDataFile, encoding="UTF-8") as f:
                jsonData = json.load(f)
            for key in self.versionInfo.keys():
                if  key in jsonData.keys():
                    self.versionInfo[key] = jsonData[key]
                    #print(key, self.versionInfo[key])
        except:
            traceback.print_exc()
            print ("onLoadJson: Fail")
            return False
        
        return True
        
    def _makeVersionFile(self):
        print("_makeVersionFile")
        self.initVersionInfo()
        
    def initVersionInfo(self):
        self.versionInfo = {}
        self.versionInfo['filename'] = "version.py"
        self.versionInfo['header'] = 'SW_VERSION="V0.1105'
        self.versionInfo['separator'] = "."
        self.versionInfo['date'] = "TE"
        self.versionInfo['month_release_count'] = 1
        self.versionInfo['tail'] = '"'

def main(): 
    versionInfo = VersionInfo()
    versionInfo.updateVersionInfo()

if __name__ == '__main__':
    main()

