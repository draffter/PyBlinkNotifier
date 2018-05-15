# -*- coding: utf-8 -*-
import configparser
import codecs


class Config(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.parse_config()

    def parse_config(self):
        self.config.read('config.ini')
        # with codecs.open('config.ini', 'r', encoding='utf-8') as f:
        #     self.config.readfp(f)

    def get_string(self, section, option):
        return self.config.get(section, option)

    def get_int(self, section, option):
        return self.config.getint(section, option)

    def get_bool(self, section, option):
        return self.config.getboolean(section, option)
