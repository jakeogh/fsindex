#!/usr/bin/env python3

import click
from kcl.printops import eprint
from fsindex.cli._create._record import _record
from fsindex.cli._create._index import _index

@click.group()
def _create():
    pass

_create.add_command(_record, name='record')
_create.add_command(_index, name='index')
