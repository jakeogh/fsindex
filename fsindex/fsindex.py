#!/usr/bin/env python3

# https://github.com/pallets/click/issues/891#issuecomment-358594289

import click
import builtins
from fsindex.model.Config import CONFIG
builtins.config = CONFIG

from kcl.sqlalchemy.clickapp.clickapp import clickapp as fsindex
fsindex.help = CONFIG.appname + " interface"
CONFIG.appobject = fsindex

from kcl.sqlalchemy.clickapp.default import *

from .cli.visualization.sa_display import sa_display
from .cli._list._list import _list
from .cli._create._create import _create
from .cli._find._find import _find

fsindex.add_command(sa_display)
fsindex.add_command(_list, name='list')
fsindex.add_command(_create, name='create')
fsindex.add_command(_find, name='find')


##!/usr/bin/env python3
#
#import shutil
#import sys
#import os
#import hashlib
#import pprint
#from stat import *
#import click
#from kcl.printops import eprint
#from kcl.fileops import path_exists
#from .update import update_db
#from .db_operations import db_stats
#from .db_connection import get_db_connection
#
#DB_PATH = '/poolz3_8x5TB_A/__fsindex/_good/fsindex.sha1.db'
#c = get_db_connection(DB_PATH)
#
#from .db_operations import FIELDS
#from .db_operations import MODE_FUNCTIONS
#PP = pprint.PrettyPrinter(indent=4)
#
#CONTEXT_SETTINGS = \
#    dict(help_option_names=['--help'],
#         terminal_width=shutil.get_terminal_size((80, 20)).columns)
#
#def matching_mode(result, modes):
#    for modefunc in modes:
#        code = modefunc+'('+str(result[4])+')'
#        answer = eval(code)
#        if answer:
#            return True
#
#@click.group(chain=True)
#@click.pass_context
#def cli(ctx):
#    """Interface to fsindex.
#    Example:
#    \b
#        fsindex search --field file_name --term test.txt display
#    """
#
#@cli.resultcallback()
#def process_commands(processors):
#    """This result callback is invoked with an iterable of all the chained
#    subcommands.  As in this example each subcommand returns a function
#    we can chain them together to feed one into the other, similar to how
#    a pipe on unix works.
#    From: https://github.com/pallets/click/blob/master/examples/imagepipe/imagepipe.py
#    """
#    # Start with an empty iterable.
#    stream = ()
#
#    # Pipe it through all stream processors.
#    for processor in processors:
#        stream = processor(stream)
#
#    # Evaluate the stream and throw away the items.
#    for _ in stream:
#        pass
#
#@cli.command('dupes')
#@click.option('--file', 'infile', required=True, nargs=1)
#@click.option('--verbose', is_flag=True)
#@generator
#def dupes(infile, verbose):
#    infile = bytes(infile, 'UTF8')
#    if verbose: eprint(infile)
#    infile = os.path.realpath(infile)
#    with open(infile, 'rb') as fh:
#        infilehash = hashlib.sha1(fh.read()).hexdigest()
#    results = match_field(field='data_hash', term=infilehash, substring=False)
#    for result in results:
#        yield result
#
#
#@cli.command('exists')
#@processor
#def exists(results):
#    for result in results:
#        if not path_exists(result[1]):
#            continue
#        yield result
#
#@cli.command('mode')
#@click.option('--mode', 'modes', is_flag=False, nargs=1, type=click.Choice(list(MODE_FUNCTIONS.keys())),
#              required=True, multiple=True)
#@processor
#def mode(results, modes):
#    for result in results:
#        if modes:
#            if not matching_mode(result, modes):
#                continue
#        yield result
#
#@cli.command('show')
#@processor
#def show(results):
#    for result in results:
#        newline = False
#        for field in result:
#            newline = True
#            if isinstance(field, bytes):
#                sys.stdout.buffer.write(field + b' ')
#            else:
#                print(field, end=' ')
#        if newline:
#            print('\n', end='')
#            newline = False
#        yield result
#
#@cli.command('fields')
#@click.option('--field', 'fields', is_flag=False, nargs=1, type=click.Choice(list(FIELDS.keys())),
#              required=True, multiple=True)
#@processor
#def fields(results, fields):
#    for result in results:
#        new_result = []
#        for index, rfield in enumerate(FIELDS.keys()):
#            if rfield in fields or not fields:
#                new_result.append(result[index])
#        yield new_result
#
#@cli.command('pprint')
#@processor
#def p_print(results):
#    for result in results:
#        PP.pprint(result)
#        yield result
#
#@cli.command('bool')
#@click.option('--verbose', is_flag=True)
#@processor
#def result_bool(results, verbose):
#    for result in results:
#        if verbose: eprint(True)
#        #yield True
#        quit(0)
#    if verbose: eprint(False)
#    #yield False
#    quit(1)
#
#@cli.command()
#def listfields():
#    PP.pprint(FIELDS)
#    quit(0)
#
#@cli.command()
#def listmodes():
#    PP.pprint(MODE_FUNCTIONS)
#    quit(0)
#
#@cli.command()
#def stats():
#    #print(db_stats())
#    session.execute('select name from sqlite_master where type=\'table\'')
#    for table in c:
#        print(table[0])
#    session.execute('select * from sqlite_master')
#    for thing in c:
#        print(thing)
#    quit(0)
#
#@cli.command()
#@click.option('--root', required=True, nargs=1)
#def update(root):
#    update_db(root)
#    quit(0)
#
