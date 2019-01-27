#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MIT License
'''
    Config class
'''
import attr
#import typing
from kcl.sqlalchemy.model.BaseConfig import BaseConfig

@attr.s(auto_attribs=True)
class Config(BaseConfig):
    '''Simple configuration class.'''
    appname: str = "fsindex"
    def __attrs_post_init__(self):
        BaseConfig.__init__(self)

CONFIG = Config()
