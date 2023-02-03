import logging.handlers
from ui.MemoUIFrame import *
from manager.MemoManager import MemoManager
from buildinfo.info import *
'''
Start  : 2019.12.05
Update : 2020.01.15
'''


def init_logger():
    logger = logging.getLogger("chobomemo")
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s [%(levelno)d] %(filename)s %(funcName)s > %(message)s')
    
    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    logger.addHandler(stream_hander)
    
    need_file_logging = os.path.exists(".\\needlog.txt")
    if need_file_logging:
        max_log_size = 128 * 1024
        file_handler = logging.handlers.RotatingFileHandler(filename='./minim.log', maxBytes=max_log_size)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    logger.info('=== ' + SW_VERSION + ' ===')


def print_end():
    logger = logging.getLogger("chobomemo")
    logger.info('=== END ===')


def main():
    app = wx.App()

    progress_bar = wx.ProgressDialog("Create DB", "Please wait", maximum=100, parent=None,
                                          style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)
    memoManager = MemoManager(progress_bar)
    progress_bar.Destroy()
    progress_bar = None

    frm = MemoUIFrame(None, swVersion=SW_VERSION, size=(800,600))
    frm.OnSetMemoManager(memoManager)
    memoManager.OnRegister(frm)
    frm.Show()
    app.MainLoop()
    memoManager.OnSave()


if __name__ == '__main__':
    init_logger()
    main()
    print_end()