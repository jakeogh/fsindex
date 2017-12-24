#!/usr/bin/env python3

import click
import shutil
from sqlalchemy_utils.functions import database_exists
from sqlalchemy_utils.functions import create_database
from kcl.logops import set_verbose
from kcl.printops import eprint
from kcl.sqlalchemy.test import test as kcltest
from kcl.sqlalchemy.print_database import print_database
from kcl.sqlalchemy.self_contained_session import self_contained_session
from kcl.sqlalchemy.BaseMixin import BASE
from kcl.sqlalchemy.model.Config import CONFIG
from kcl.click.CONTEXT_SETTINGS import CONTEXT_SETTINGS
from .cli.list_objects.list_objects import list_objects
from .cli.create_objects.create_objects import create_objects

__version__ = 0.01

# pylint: disable=C0326
# http://pylint-messages.wikidot.com/messages:c0326
@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--verbose', is_flag=True, callback=set_verbose, expose_value=True)
@click.option('--database', is_flag=False, type=str, required=False)
@click.option('--temp-database', is_flag=True, required=False)
@click.pass_context
def fsindex(ctx, verbose, database, temp_database):
    ''' fsindex orm interface'''
    if temp_database:
        CONFIG.database = CONFIG.database_timestamp
    else:
        CONFIG.database = CONFIG.database_real('fsindex')
    if verbose:
        print("verbose is True")
        eprint(CONFIG.database)
    if not database_exists(CONFIG.database):
        create_database(CONFIG.database)
        with self_contained_session(CONFIG.database) as session:
            BASE.metadata.create_all(session.bind)
    if verbose:
        eprint(CONFIG.database)
    ctx.obj = CONFIG
    pass

@fsindex.command()
@click.option('--package', is_flag=False, type=str, required=False, default='fsindex')
@click.option('--keep-databases', is_flag=True)
@click.option('--count', is_flag=False, type=int, required=False)
@click.option('--test-class', is_flag=False, type=str, required=False)
@click.option('--test-match', is_flag=False, type=str, required=False)
def test(package, keep_databases, count, test_class, test_match):
    kcltest(package=package, keep_databases=keep_databases, count=count, test_class=test_class, test_match=test_match)

fsindex.add_command(list_objects, name='list')
fsindex.add_command(create_objects, name='create')
fsindex.add_command(print_database)

#fsindex.add_command(bookmark)
#fsindex.add_command(content_files)
#fsindex.add_command(show_config, name='config')
#fsindex.add_command(display_database)
#fsindex.add_command(ipython)
#fsindex.add_command(import_all_iris)
