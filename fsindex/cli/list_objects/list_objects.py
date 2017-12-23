#!/usr/bin/env python3

import click
from kcl.printops import eprint
from fsindex.cli.list_objects.filerecord import filerecord

@click.group()
def list_objects():
    pass

list_objects.add_command(filerecord, name='records')
