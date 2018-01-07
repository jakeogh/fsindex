#!/usr/bin/env python3

import click
from kcl.printops import eprint
from fsindex.cli._create.filerecord import filerecord
from fsindex.cli._create.filerecord_index import filerecord_index

@click.group()
def _create():
    pass

_create.add_command(filerecord, name='record')
_create.add_command(filerecord_index, name='index')
