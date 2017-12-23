#!/usr/bin/env python3

import click
from kcl.printops import eprint
from fsindex.cli.create_objects.filerecord import filerecord

@click.group()
def create_objects():
    pass

create_objects.add_command(filerecord, name='record')
