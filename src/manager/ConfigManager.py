#!/usr/bin/python
#-*- coding: utf-8 -*-

import util.fileutil as fileutil


class ConfigManager:
    def __init__(self):
        self.config = {}
        self._init_cfg_data()
        self.is_update = False

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
        self.config['ctrl_i'] = "#8282"
        self.config['memo'] = ""
        self.config['WINDOW_SIZE_W'] = 800
        self.config['WINDOW_SIZE_H'] = 600
        self.config['AND'] = ','
        self.config['OR'] = '|'
        self.config['ask_before_quit'] = False
        self.config['compressedSave'] = False
        self.config['save_cfm'] = False

        cfg_data = fileutil.load_config('./minim.cfg')
        for key, item in self.config.items():
            self.config[key] = cfg_data.get(key, item)

        bool_list = ['ask_before_quit', 'compressedSave', 'save_cfm']
        for item in bool_list:
            if type(self.config[item]) == str:
                self.config[item] = 'true' in self.config[item]
                self.is_update = True

    def GetValue(self, key):
        return self.config.get(key, [])

    def SetValue(self, key):
        self.config['ctrl_0'] = key['ctrl_0']
        self.config['ctrl_1'] = key['ctrl_1']
        self.config['ctrl_2'] = key['ctrl_2']
        self.config['ctrl_3'] = key['ctrl_3']
        self.config['ctrl_4'] = key['ctrl_4']
        self.config['ctrl_5'] = key['ctrl_5']
        self.config['ctrl_6'] = key['ctrl_6']
        self.config['ctrl_7'] = key['ctrl_7']
        self.config['ctrl_8'] = key['ctrl_8']
        self.config['ctrl_9'] = key['ctrl_9']
        self.config['ctrl_i'] = key['ctrl_i']
        self.config['memo'] = key['memo']
        self.config['ask_before_quit'] = key['ask_before_quit']
        self.config['compressedSave'] = key['compressedSave']
        self.config['save_cfm'] = key['save_cfm']
        self.is_update = True

    def SetMemo(self, data):
        self.config['memo'] = data
        self.is_update = True

    def get_all_config(self):
        return self.config.copy()

    def save(self):
        if self.is_update:
            print("[ConfigManager] save")
            fileutil.saveAsJson(self.config, './minim.cfg', 2)
            self.is_update = False
        else:
            print("[ConfigManager] not updated! Skip save!")

    def get_ctrl_value(self):
        ctrl_list = ['ctrl_i', 'ctrl_1', 'ctrl_2', 'ctrl_3', 'ctrl_4', 'ctrl_5',
                     'ctrl_6', 'ctrl_7', 'ctrl_8', 'ctrl_9', 'ctrl_0']
        result = []
        for i in ctrl_list:
            result.append(self.config[i])

        return result