#!/usr/bin/env python3

import click
from kcl.printops import eprint
from fsindex.cli.find.filename import filename
from fsindex.cli.find.path import path

@click.group()
def find():
    pass

find.add_command(filename)
find.add_command(path)
