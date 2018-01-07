#!/usr/bin/env python3

import click
from kcl.sqlalchemy.self_contained_session import self_contained_session
from kcl.sqlalchemy.model.Filename import Filename

@click.command()
@click.pass_obj
def filenames(config):
    with self_contained_session(config.database) as session:
        filenames_generator = session.query(Filename)
        for filenames in filenames_generator:
            print(filenames)
