#!/usr/bin/env python3

import configparser
import os

home = os.path.expanduser("~")
config_folder = home + '/.fsindex'
config_file = config_folder + '/fsindex_config'

def write_default_config_file():
    config['DATABASE'] = {'Location': database_location,
                          'Compression': 'TODO',
                          'CompressionLevel': 'TODO'}
    with open(config_file, 'w') as configfile:
        config.write(configfile)
    return True

def read_config_file(config_file=config_file):
    #race condition, config.read throws no error when it trys to read empty or non existing config file...
    if os.path.isfile(config_file) and is_non_zero_file(config_file):
        config.read(config_file)
        return config
    else:
        print("Problem reading config file, creating default config.")
        write_default_config_file()
        config.read(config_file)
        return config

class Config_FSindex():
    def __init__(self, config_file=config_file):
        self.config             = read_config_file(config_file)
        self.database_folder    = self.config['DATABASE']['location']
        self.hash_length        = 40
