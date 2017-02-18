#!/usr/bin/env python3

import click
import shutil
import glob
import sys
import os
import pickle
import hashlib
import pprint
from functools import update_wrapper
from stat import *

from kcl.printops import cprint
from kcl.printops import seprint
from kcl.printops import set_verbose
from kcl.fileops import path_exists
from .update import update_db
from .db_operations import db_stats
from .db_connection import c
from .db_operations import FIELDS
from .db_operations import MODE_FUNCTIONS

pp = pprint.PrettyPrinter(indent=4)

CONTEXT_SETTINGS = \
    dict(help_option_names=['--help'],
         terminal_width=shutil.get_terminal_size((80, 20)).columns)

@click.group(chain=True)
def cli():
    """This script processes a bunch of images through pillow in a unix
    pipe.  One commands feeds into the next.
    Example:
    \b
        imagepipe open -i example01.jpg resize -w 128 display
        imagepipe open -i example02.jpg blur save
    """

@cli.resultcallback()
def process_commands(processors):
    """This result callback is invoked with an iterable of all the chained
    subcommands.  As in this example each subcommand returns a function
    we can chain them together to feed one into the other, similar to how
    a pipe on unix works.
    """
    # Start with an empty iterable.
    stream = ()

    # Pipe it through all stream processors.
    for processor in processors:
        stream = processor(stream)

    # Evaluate the stream and throw away the items.
    for _ in stream:
        pass

def processor(f):
    """Helper decorator to rewrite a function so that it returns another
    function from it.
    """
    def new_func(*args, **kwargs):
        def processor(stream):
            return f(stream, *args, **kwargs)
        return processor
    return update_wrapper(new_func, f)


def generator(f):
    """Similar to the :func:`processor` but passes through old values
    unchanged and does not pass through the values as parameter.
    """
    @processor
    def new_func(stream, *args, **kwargs):
        for item in stream:
            yield item
        for item in f(*args, **kwargs):
            yield item
    return update_wrapper(new_func, f)



@cli.command('search')
@click.option('--field', required=True, nargs=1, type=click.Choice(list(FIELDS.keys())))
@click.option('--term', required=True, nargs=1)
@click.option('--substring', is_flag=True)
@generator
def search(field, term, substring):
    if FIELDS[field] == 'BLOB':
        term = bytes(term, 'UTF8')
    elif FIELDS[field] == 'INT':
        term = int(term)
    #print("field:", field)
    #print("term:", term)
    if 'hash' in field:
        term = term.lower()
    if substring:
        query = '''SELECT * FROM path_db WHERE ''' + field + ''' LIKE ?'''
        answer = c.execute(query, (b'%'+term+b'%',))
    else:
        query = '''SELECT * FROM path_db WHERE ''' + field + '''=?'''
        answer = c.execute(query, (term,))

    results = answer.fetchall()
    count = len(results)
    seprint("count:", "{:,}".format(count))
    for result in results:
        yield result


def matching_mode(result, modes):
    for modefunc in modes:
        code = modefunc+'('+str(result[4])+')'
        answer = eval(code)
        if answer:
            return True


@cli.command('filter')
@click.option('--exists', is_flag=True)
@click.option('--mode', 'modes', is_flag=False, nargs=1,
              type=click.Choice(list(MODE_FUNCTIONS.keys())),
              required=False, multiple=True)
@processor
def filter(results, exists, modes):
    #assert not (exists and modes)
    for result in results:
        if exists:
            if not path_exists(result[1]):
                continue
        if modes:
            if not matching_mode(result, modes):
                continue
        print(result)
        yield result


@cli.command('display')
@processor
def display(results):
    for result in results:
        print(result)
        yield result

@cli.command()
def listfields():
    pp.pprint(FIELDS)

@cli.command()
def listmodes():
    pp.pprint(MODE_FUNCTIONS)

@cli.command()
def stats():
    #print(db_stats())
    c.execute('select name from sqlite_master where type=\'table\'')
    for table in c:
        print(table[0])
    c.execute('select * from sqlite_master')
    for thing in c:
        print(thing)




#
#def match_field(field, term, resultfields, exists, substring, modes):
#    if 'hash' in field:
#        term = term.lower()
#    if substring:
#        query = '''SELECT * FROM path_db WHERE ''' + field + ''' LIKE ?'''
#        answer = c.execute(query, (b'%'+term+b'%',))
#    else:
#        query = '''SELECT * FROM path_db WHERE ''' + field + '''=?'''
#        answer = c.execute(query, (term,))
#
#    results = answer.fetchall()
#
#    filtered_count = 0
#    for result in results:
#        if exists:
#            if not path_exists(result[1]):
#                continue
#        valid_mode = False
#        if modes:
#            if matching_mode(result, modes):
#                valid_mode = True
#        if modes:
#            if not valid_mode:
#                continue
#
#        newline = False
#        for index, rfield in enumerate(FIELDS.keys()):
#            if rfield in resultfields or not resultfields:
#                newline = True
#                if isinstance(result[index], bytes):
#                    sys.stdout.buffer.write(result[index] + b' ')
#                else:
#                    print(result[index], end=' ')
#        if newline:
#            filtered_count += 1
#            print('\n', end='')
#            newline = False
#
#    count = len(results)
#    seprint("original count:", "{:,}".format(count))
#    seprint("filtered_count:", "{:,}".format(filtered_count))
#    seprint("\n", end='')
#
#
#@click.group(context_settings=CONTEXT_SETTINGS)
#@click.option('--verbose', is_flag=True, callback=set_verbose, expose_value=False)
#@click.pass_context
#def fsindex(ctx):
#    pass
#
#@fsindex.command()
#@click.argument('root', required=True, nargs=1)
#@click.pass_context
#def update(root):
#    update_db(root)
#
#
#
#@fsindex.command()
#@click.argument('results', required=True, nargs=-1, type=click.File('rb'))
#@click.option('--exists', is_flag=True)
#@click.option('--mode', is_flag=False, nargs=1,
#              type=click.Choice(list(MODE_FUNCTIONS.keys())),
#              required=False, multiple=True)
#@click.pass_context
#def filter(ctx, results, exists, mode):
#
#
#    for result in results:
#        print("filter():", result)
#
#
#@fsindex.command()
#@click.argument('field', required=True, nargs=1)
#@click.argument('term', required=True, nargs=1)
#@click.argument('resultfields', required=False, nargs=-1)
#@click.option('--exists', is_flag=True)
#@click.option('--substring', is_flag=True)
#@click.option('--mode', is_flag=False, nargs=1,
#              type=click.Choice(list(MODE_FUNCTIONS.keys())),
#              required=False, multiple=True)
#@click.option('--verbose', is_flag=True)
#@click.pass_context
#def old_search(ctx, field, term, resultfields, exists, substring, mode, verbose):
#    modes = mode
#    assert field in FIELDS.keys()
#    if verbose: seprint("field:", field)
#    if verbose: seprint("term:", term)
#    for rfield in resultfields:
#        assert rfield in FIELDS.keys()
#    if verbose: seprint("resultfields:", resultfields)
#    if verbose: seprint("exists:", exists)
#    if verbose: seprint("substring:", substring)
#    assert len(modes) <= len(MODE_FUNCTIONS.keys())
#    for mode in modes:
#        #print("mode:", mode)
#        assert mode in MODE_FUNCTIONS.keys()
#    if verbose: seprint("modes:", modes)
#
#    if FIELDS[field] == 'BLOB':
#        term = bytes(term, 'UTF8')
#    elif FIELDS[field] == 'INT':
#        term = int(term)
#    match_field(field=field, term=term, resultfields=resultfields, exists=exists, substring=substring, modes=modes)
#
#if __name__ == '__main__':
#    # pylint: disable=no-value-for-parameter
#    fsindex()
#    # pylint: enable=no-value-for-parameter
#    #eprint("Exiting without error.", level=LOG['DEBUG'])
#
#
#def search_existing_file_hash(infile):
#    infile = bytes(infile, 'UTF8')
#    infile = os.path.realpath(infile)
#    with open(infile, 'rb') as fh:
#        infilehash = hashlib.sha1(fh.read()).hexdigest()
#    match_field(field='data_hash', term=infilehash, resultfields=('full_path',), exists=False, substring=False, modes=False)
