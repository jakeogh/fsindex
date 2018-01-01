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

from kcl.sqlalchemy.table_list import table_list
from kcl.sqlalchemy.self_contained_session import self_contained_session
from functools import update_wrapper



def processor(f):
    """Helper decorator to rewrite a function so that it returns another
    function from it.
    From: https://github.com/pallets/click/blob/master/examples/imagepipe/imagepipe.py
    """
    def new_func(*args, **kwargs):
        def processor(stream):
            return f(stream, *args, **kwargs)
        return processor
    return update_wrapper(new_func, f)

def generator(f):
    """Similar to the :func:`processor` but passes through old values
    unchanged and does not pass through the values as parameter.
    From: https://github.com/pallets/click/blob/master/examples/imagepipe/imagepipe.py
    """
    @processor
    def new_func(stream, *args, **kwargs):
        for item in stream:
            yield item
        for item in f(*args, **kwargs):
            yield item
    return update_wrapper(new_func, f)




def match_field(session, table, field, term, substring):
    tables = table_list(database=session.bind.url)
    eprint(tables)
    if table not in tables: # todo make decorator
        eprint("non existing table:", table, "valid tables:", tables)
        quit(1)

    #if FIELDS[field] == 'BLOB':
    #    if not isinstance(term, bytes):
    #        term = bytes(term, 'UTF8')
    #elif FIELDS[field] == 'INT':
    #    term = int(term)
    #if 'hash' in field:
    #    term = term.lower()
    if substring:
        query = '''SELECT * FROM ''' + table + ''' WHERE ''' + field + ''' LIKE ?'''
        try:
            answer = session.execute(query, (b'%'+term+b'%',))
        except TypeError:
            answer = session.execute(query, ('%'+term+'%',))
    else:
        query = '''SELECT * FROM ''' + table + ''' WHERE ''' + field + '''=?'''
        answer = session.execute(query, (term,))
    results = answer.fetchall()
    #count = len(results)
    #eprint("match_field() count:", "{:,}".format(count))
    return results
#
@fsindex.command('search')
#@click.option('--field', required=True, nargs=1, type=click.Choice(list(FIELDS.keys())))
@click.option('--table', required=True, nargs=1)
@click.option('--field', required=True, nargs=1)
@click.option('--term', required=True, nargs=1)
@click.option('--substring', is_flag=True)
#@generator
def search(table, field, term, substring):
    eprint(field, term, substring)
    with self_contained_session(config.database) as session:
#        BASE.metadata.create_all(session.bind)
        results = match_field(session=session, table=table, field=field, term=term, substring=substring)
        for result in results:
            print(result)
            #yield result

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
#
#
#
