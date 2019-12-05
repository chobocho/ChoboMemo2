import wx
import logging
import logging.handlers
from MemoUIFrame import *
from MemoManager import MemoManager
'''
Start  : 2019.12.05
Update : 2019.12.06
'''

SW_VERSION = "ChoboMemo v0.1105SL.1"

def initLogger():
    logger = logging.getLogger("chobomemo")
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s [%(levelno)d] %(filename)s %(funcName)s > %(message)s')
    
    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    logger.addHandler(stream_hander)
    
    max_log_size = 128 * 1024

    file_handler = logging.handlers.RotatingFileHandler(filename='./chobomemo.log', maxBytes=max_log_size)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    logger.info('=== ' + SW_VERSION + ' ===')

def printEnd():
    logger = logging.getLogger("chobomemo")
    logger.info('=== END ===')

def main(): 
    app = wx.App()
    memoManager = MemoManager()
    frm = MemoUIFrame(None, swVersion=SW_VERSION, size=(800,600))
    frm.OnRegister(memoManager)
    frm.Show()
    app.MainLoop()
    pass

if __name__ == '__main__':
    initLogger()
    main()
    printEnd()