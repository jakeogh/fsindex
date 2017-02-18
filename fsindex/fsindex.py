#!/usr/bin/env python3

import click
import shutil
import glob
import sys
import os
import pickle
import hashlib
import pprint
from stat import *

from kcl.printops import cprint
from kcl.printops import seprint
from kcl.printops import set_verbose
from kcl.fileops import path_exists
from .update import update_db
from .db_operations import db_stats
from .db_connection import c
from .db_operations import FIELDS
from .db_operations import MODES

pp = pprint.PrettyPrinter(indent=4)

CONTEXT_SETTINGS = \
    dict(help_option_names=['--help'],
         terminal_width=shutil.get_terminal_size((80, 20)).columns)

def search_existing_file_name(infile):
    assert isinstance(filename, bytes)
    infile = os.path.realpath(infile)
    filename = infile.split(b'/')[-1]
    filestat = os.stat(infile)
    answer = c.execute('''SELECT full_path, file_name, st_size FROM path_db WHERE file_name=?''', (filename,))
    for result in answer.fetchall():
        if result[0] == infile:
            continue
        if result[2] == filestat.st_size:
    #       print("filename and size match:", result)
    #       print("checking if match still exists")
            try:
                matchstat = os.stat(result[0])
            except FileNotFoundError:
    #           print("Error: No such file or directory:", result[0], "skipping")
    #           os._exit(1)
                continue
    #       print("checking hash...")
            with open(result[0], 'rb') as fh:
                matchhash = hashlib.sha1(fh.read()).hexdigest()
            with open(file, 'rb') as fh:
                filehash = hashlib.sha1(fh.read()).hexdigest()
            if matchhash == filehash:
    #           print("match found:", result[0])
                seprint(result[0])
            else:
                seprint("hashes do not match! NOT a match:", result[0])

def match_field(field, term, resultfields, exists, substring, modes):
    if 'hash' in field:
        term = term.lower()
    if substring:
        query = '''SELECT * FROM path_db WHERE ''' + field + ''' LIKE ?'''
        answer = c.execute(query, (b'%'+term+b'%',))
    else:
        query = '''SELECT * FROM path_db WHERE ''' + field + '''=?'''
        answer = c.execute(query, (term,))

    results = answer.fetchall()

    for result in results:
        newline = False
        for index, rfield in enumerate(FIELDS.keys()):
            if rfield in resultfields:
                if exists:
                    if not path_exists(result[1]):
                        continue
                if modes:
                    print("modes:", modes)
                newline = True
                if isinstance(result[index], bytes):
                    sys.stdout.buffer.write(result[index] + b' ')
                else:
                    print(result[index], end=' ')
        if newline:
            print('\n', end='')
            newline = False

    count = len(results)
    seprint("count:", count)
    seprint("\n", end='')

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--verbose', is_flag=True, callback=set_verbose, expose_value=False)
@click.pass_context
def fsindex(ctx):
    pass

@fsindex.command()
@click.argument('root', required=True, nargs=1)
@click.pass_context
def update(root):
    update_db(root)

@fsindex.command()
@click.pass_context
def listfields(ctx):
    pp.pprint(FIELDS)

@fsindex.command()
@click.pass_context
def listmodes(ctx):
    pp.pprint(MODES)

@fsindex.command()
@click.pass_context
def stats(ctx):
    #print(db_stats())
    c.execute('select name from sqlite_master where type=\'table\'')
    for table in c:
        print(table[0])
    c.execute('select * from sqlite_master')
    for thing in c:
        print(thing)

@fsindex.command()
@click.argument('field', required=True, nargs=1)
@click.argument('term', required=True, nargs=1)
@click.argument('resultfields', required=True, nargs=-1)
@click.option('--exists', is_flag=True)
@click.option('--substring', is_flag=True)
#@click.option('--modes', is_flag=False, type=click.Choice(list(MODES.keys())), required=False)
@click.option('--modes', is_flag=False, nargs=-1, required=False)
@click.pass_context
def search(ctx, field, term, resultfields, exists, substring, modes):
    assert field in FIELDS.keys()
    seprint("field:", field)
    seprint("term:", term)
    for rfield in resultfields:
        assert rfield in FIELDS.keys()
    seprint("resultfields:", resultfields)
    seprint("exists:", exists)
    seprint("substring:", substring)
    #print(MODES.keys())
    #print(list(MODES.keys()))
    assert len(modes) <= len(MODES.keys())
    for mode in modes:
        print("mode:", mode)
        assert mode in MODES.keys()
    seprint("modes:", modes)

    if FIELDS[field] == 'BLOB':
        term = bytes(term, 'UTF8')
    elif FIELDS[field] == 'INT':
        term = int(term)
    match_field(field=field, term=term, resultfields=resultfields, exists=exists, substring=substring, modes=modes)

if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    fsindex()
    # pylint: enable=no-value-for-parameter
    #eprint("Exiting without error.", level=LOG['DEBUG'])

