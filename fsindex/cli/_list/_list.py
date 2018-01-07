#!/usr/bin/env python3

import click
from kcl.printops import eprint
from fsindex.cli._list.filerecord import filerecord
from fsindex.cli._list.filename import filename
from fsindex.cli._list.path import path

@click.group()
def _list():
    pass

_list.add_command(filerecord, name='records')
_list.add_command(filename, name='filenames')
_list.add_command(path, name='paths')
