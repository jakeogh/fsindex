#!/usr/bin/env python3

import click
from kcl.printops import eprint
from iridb.model.Tag import Tag
from kcl.sqlalchemy.self_contained_session import self_contained_session
from fsindex.cli.list_objects.filerecords import filerecords

@click.group()
def list_objects():
    pass


list_objects.add_command(list_filerecords, name='records')
