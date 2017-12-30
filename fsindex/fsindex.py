#!/usr/bin/env python3

import click
import builtins
from fsindex.model.Config import CONFIG
builtins.config = CONFIG

from kcl.sqlalchemy.clickapp.clickapp import clickapp as fsindex
from kcl.sqlalchemy.clickapp.test import test
from kcl.sqlalchemy.ipython import ipython
from .cli.visualization.sa_display import sa_display
from .cli.list_objects.list_objects import list_objects
from .cli.create_objects.create_objects import create_objects

fsindex.help = CONFIG.appname + " interface"

#@fsindex.command()
#@click.option('--package', is_flag=False, type=str, required=False, default='fsindex')
#@click.option('--keep-databases', is_flag=True)
#@click.option('--count', is_flag=False, type=int, required=False)
#@click.option('--test-class', is_flag=False, type=str, required=False)
#@click.option('--test-match', is_flag=False, type=str, required=False)
#def test(package, keep_databases, count, test_class, test_match):
#    kcltest(package=package, keep_databases=keep_databases, count=count, test_class=test_class, test_match=test_match)

@fsindex.command()
@click.option('--table', type=str, default=False)
@click.pass_context
def print_database(ctx, table):
    ctx.invoke(kcl_print_database, database=ctx.obj.database, table=table)

fsindex.add_command(list_objects, name='list')
fsindex.add_command(create_objects, name='create')
fsindex.add_command(ipython)
fsindex.add_command(sa_display)

#fsindex.add_command(show_config, name='config')
#fsindex.add_command(display_database)
fsindex.add_command(test)

