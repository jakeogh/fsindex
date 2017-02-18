#!/usr/bin/env python3

import shutil
import sys
import os
import hashlib
import pprint
from functools import update_wrapper
from stat import *
import click
from kcl.printops import seprint
from kcl.fileops import path_exists
from .update import update_db
from .db_operations import db_stats
from .db_connection import c
from .db_operations import FIELDS
from .db_operations import MODE_FUNCTIONS
PP = pprint.PrettyPrinter(indent=4)

CONTEXT_SETTINGS = \
    dict(help_option_names=['--help'],
         terminal_width=shutil.get_terminal_size((80, 20)).columns)

def matching_mode(result, modes):
    for modefunc in modes:
        code = modefunc+'('+str(result[4])+')'
        answer = eval(code)
        if answer:
            return True

@click.group(chain=True)
@click.pass_context
def cli(ctx):
    """Interface to fsindex.
    Example:
    \b
        fsindex search --field file_name --term test.txt display
    """

@cli.resultcallback()
def process_commands(processors):
    """This result callback is invoked with an iterable of all the chained
    subcommands.  As in this example each subcommand returns a function
    we can chain them together to feed one into the other, similar to how
    a pipe on unix works.
    From: https://github.com/pallets/click/blob/master/examples/imagepipe/imagepipe.py
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

@cli.command('dupes')
@click.option('--file', 'infile', required=True, nargs=1)
@click.option('--verbose', is_flag=True)
@generator
def dupes(infile, verbose):
    infile = bytes(infile, 'UTF8')
    if verbose: seprint(infile)
    infile = os.path.realpath(infile)
    with open(infile, 'rb') as fh:
        infilehash = hashlib.sha1(fh.read()).hexdigest()
    results = match_field(field='data_hash', term=infilehash, substring=False)
    for result in results:
        yield result

def match_field(field, term, substring):
    if FIELDS[field] == 'BLOB':
        if not isinstance(term, bytes):
            term = bytes(term, 'UTF8')
    elif FIELDS[field] == 'INT':
        term = int(term)
    if 'hash' in field:
        term = term.lower()
    if substring:
        query = '''SELECT * FROM path_db WHERE ''' + field + ''' LIKE ?'''
        try:
            answer = c.execute(query, (b'%'+term+b'%',))
        except TypeError:
            answer = c.execute(query, ('%'+term+'%',))
    else:
        query = '''SELECT * FROM path_db WHERE ''' + field + '''=?'''
        answer = c.execute(query, (term,))
    results = answer.fetchall()
    #count = len(results)
    #seprint("match_field() count:", "{:,}".format(count))
    return results

@cli.command('search')
@click.option('--field', required=True, nargs=1, type=click.Choice(list(FIELDS.keys())))
@click.option('--term', required=True, nargs=1)
@click.option('--substring', is_flag=True)
@generator
def search(field, term, substring):
    results = match_field(field=field, term=term, substring=substring)
    for result in results:
        yield result

@cli.command('exists')
@processor
def exists(results):
    for result in results:
        if not path_exists(result[1]):
            continue
        yield result

@cli.command('mode')
@click.option('--mode', 'modes', is_flag=False, nargs=1,
              type=click.Choice(list(MODE_FUNCTIONS.keys())),
              required=False, multiple=True)
@processor
def mode(results, modes):
    for result in results:
        if modes:
            if not matching_mode(result, modes):
                continue
        yield result

@cli.command('display')
@click.option('--field', 'fields', is_flag=False, nargs=1,
              type=click.Choice(list(FIELDS.keys())),
              required=False, multiple=True)
@processor
def display(results, fields):
    seprint("fields:", fields)
    for result in results:
        newline = False
        for index, rfield in enumerate(FIELDS.keys()):
            if rfield in fields or not fields:
                newline = True
                if isinstance(result[index], bytes):
                    sys.stdout.buffer.write(result[index] + b' ')
                else:
                    print(result[index], end=' ')
        if newline:
            print('\n', end='')
            newline = False
        yield result

@cli.command('path')
@processor
@click.pass_context
def path(ctx, results):
    #print("ctx:", ctx)
    #print("type(ctx):", type(ctx))
    #for thing in ctx:
    #    print(thing)
    #ctx.invoke(display, results=results, fields=('full_path',))
    ctx.forward(display)

@cli.command('bool')
@click.option('--verbose', is_flag=True)
@processor
def result_bool(results, verbose):
    for result in results:
        if verbose: seprint(True)
        #yield True
        quit(0)
    if verbose: seprint(False)
    #yield False
    quit(1)

@cli.command()
def listfields():
    PP.pprint(FIELDS)
    quit(0)

@cli.command()
def listmodes():
    PP.pprint(MODE_FUNCTIONS)
    quit(0)

@cli.command()
def stats():
    #print(db_stats())
    c.execute('select name from sqlite_master where type=\'table\'')
    for table in c:
        print(table[0])
    c.execute('select * from sqlite_master')
    for thing in c:
        print(thing)
    quit(0)

@cli.command()
@click.option('--root', required=True, nargs=1)
def update(root):
    update_db(root)
    quit(0)
