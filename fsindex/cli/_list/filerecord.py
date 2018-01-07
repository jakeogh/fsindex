#!/usr/bin/env python3

import click
from kcl.sqlalchemy.self_contained_session import self_contained_session
from kcl.sqlalchemy.model.FileRecord import FileRecord

@click.command()
@click.pass_obj
def filerecord(config):
    with self_contained_session(config.database) as session:
        filerecord_generator = session.query(FileRecord)
        for filerecord in filerecord_generator:
            print(filerecord)
