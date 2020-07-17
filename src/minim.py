import logging.handlers
from ui.MemoUIFrame import *
from manager.MemoManager import MemoManager
from buildinfo.info import *
'''
Start  : 2019.12.05
Update : 2020.01.15
'''

def initLogger():
    logger = logging.getLogger("chobomemo")
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s [%(levelno)d] %(filename)s %(funcName)s > %(message)s')
    
    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    logger.addHandler(stream_hander)
    
    needFileLogging = os.path.exists(".\\needlog.txt")
    if needFileLogging:
        max_log_size = 128 * 1024
        file_handler = logging.handlers.RotatingFileHandler(filename='./minim.log', maxBytes=max_log_size)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    logger.info('=== ' + SW_VERSION + ' ===')

def printEnd():
    logger = logging.getLogger("chobomemo")
    logger.info('=== END ===')

def main(): 
    memoManager = MemoManager()
    app = wx.App()
    frm = MemoUIFrame(None, swVersion=SW_VERSION, size=(800,600))
    frm.OnSetMemoManager(memoManager)
    memoManager.OnRegister(frm)
    frm.Show()
    app.MainLoop()
    memoManager.OnSave()

if __name__ == '__main__':
    initLogger()
    main()
    printEnd()