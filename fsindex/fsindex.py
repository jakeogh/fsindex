#!/usr/bin/env python3

import click
import shutil
import glob
import sys
import os
import pickle
import hashlib

from kcl.printops import cprint
from kcl.printops import set_verbose
from .update import update_db
from .db_operations import db_stats
from .db_connection import c

CONTEXT_SETTINGS = \
    dict(help_option_names=['--help'],
         terminal_width=shutil.get_terminal_size((80, 20)).columns)

def search_file_name(filename):
    print("searching for:", filename)
    answer = c.execute('''SELECT full_path, file_name, st_size FROM path_db WHERE file_name=?''', (filename,))
    for result in answer.fetchall():
        print(result)

def search_existing_file_name(infile):
    infile = os.path.realpath(infile)
    filename = infile.split('/')[-1]
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
                print(result[0])
            else:
                print("hashes do not match! NOT a match:", result[0])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--verbose', is_flag=True, callback=set_verbose, expose_value=False)
@click.pass_context
def fsindex(ctx):
    cprint("ctx:", ctx)

@fsindex.command()
@click.argument('root', required=True, nargs=1)
@click.pass_context
def update(root):
    update_db(root)

@click.pass_context
def stats(ctx):
    print(db_stats())
    c.execute('select name from sqlite_master where type=\'table\'')
    for table in c:
        print(table[0])

@click.argument('term', required=True, nargs=1)
#@click.option('--verbose', is_flag=True, required=False, callback=set_verbose, expose_value=False)
@click.option('--name', is_flag=True)
@click.option('--sha1hash', is_flag=True)
@fsindex.command()
@click.pass_context
def search(ctx, term, name, sha1hash):
    if name:
        search_file_name(term)



if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    fsindex()
    # pylint: enable=no-value-for-parameter
    eprint("Exiting without error.", level=LOG['DEBUG'])
