#!/usr/bin/env python3

import click
from kcl.printops import eprint
from fsindex.cli.list_objects.filerecord import filerecord
from fsindex.cli.list_objects.filename import filename
from fsindex.cli.list_objects.path import path

@click.group()
def list_objects():
    pass


list_objects.add_command(filerecord, name='records')
list_objects.add_command(filename, name='filenames')
list_objects.add_command(path, name='paths')
