#!/usr/bin/python
#-*- coding: utf-8 -*-

class ConfigManager:
    def __init__(self):
        self.config = {}
        self.config['ctrl_1'] = "#BookMark|#8282"
        self.config['WINDOW_SIZE_W'] = 800
        self.config['WINDOW_SIZE_H'] = 600

    def GetValue(self, key):
        return self.config.get(key, [])
