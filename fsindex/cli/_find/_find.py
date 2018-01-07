#!/usr/bin/env python3

import click
from kcl.printops import eprint
from fsindex.cli._find.filename import filename
from fsindex.cli._find.path import path

@click.group()
def _find():
    pass

_find.add_command(filename)
_find.add_command(path)
