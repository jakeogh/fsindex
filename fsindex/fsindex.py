#!/usr/bin/env python3

import click
import builtins
from fsindex.model.Config import CONFIG
builtins.config = CONFIG

from kcl.sqlalchemy.clickapp.clickapp import clickapp as fsindex
from kcl.sqlalchemy.clickapp.print_database import print_database
from kcl.sqlalchemy.clickapp.test import test
from kcl.sqlalchemy.clickapp.show_config import show_config
from kcl.sqlalchemy.ipython import ipython
from .cli.visualization.sa_display import sa_display
from .cli.list_objects.list_objects import list_objects
from .cli.create_objects.create_objects import create_objects

fsindex.help = CONFIG.appname + " interface"

fsindex.add_command(list_objects, name='list')
fsindex.add_command(create_objects, name='create')
fsindex.add_command(ipython)
fsindex.add_command(sa_display)
fsindex.add_command(print_database)

#fsindex.add_command(show_config, name='config')
#fsindex.add_command(display_database)
fsindex.add_command(test)
fsindex.add_command(show_config, name="config")

