#!/usr/bin/python
#-*- coding: utf-8 -*-

import util.fileutil as fileutil

class ConfigManager:
    def __init__(self):
        self.config = {}
        self._init_cfg_data()


    def _init_cfg_data(self):
        self.config['ctrl_1'] = "#BookMark|#8282"
        self.config['ctrl_2'] = "#1234"
        self.config['ctrl_3'] = "#Todo"
        self.config['ctrl_4'] = ""
        self.config['ctrl_5'] = ""
        self.config['ctrl_6'] = ""
        self.config['ctrl_7'] = ""
        self.config['ctrl_8'] = ""
        self.config['ctrl_9'] = ""
        self.config['ctrl_0'] = ""
        self.config['WINDOW_SIZE_W'] = 800
        self.config['WINDOW_SIZE_H'] = 600
        self.config['AND'] = '&'
        self.config['OR'] = '|'
        self.config['compressedSave'] = False

        cfg_data = fileutil.load_config('./minim.cfg')
        for key, item in self.config.items():
            self.config[key] = cfg_data.get(key, item)


    def GetValue(self, key):
        return self.config.get(key, [])


    def get_all_config(self):
        return self.config.copy()