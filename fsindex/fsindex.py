#!/usr/bin/env python3

import click
import builtins
from fsindex.model.Config import CONFIG
builtins.config = CONFIG

from kcl.sqlalchemy.clickapp.clickapp import clickapp as fsindex
fsindex.help = CONFIG.appname + " interface"
CONFIG.appobject = fsindex

from kcl.sqlalchemy.clickapp.default import *

from .cli.visualization.sa_display import sa_display
from .cli.list_objects.list_objects import list_objects
from .cli.create_objects.create_objects import create_objects
from .cli.find.find import find

fsindex.add_command(sa_display)
fsindex.add_command(list_objects, name='list')
fsindex.add_command(create_objects, name='create')
fsindex.add_command(find)

#fsindex.add_command(display_database)
