#!/usr/bin/env python3

import click
from kcl.sqlalchemy.self_contained_session import self_contained_session
from kcl.sqlalchemy.model.Path import Path

@click.command()
@click.pass_obj
def path(config):
    with self_contained_session(config.database) as session:
        path_generator = session.query(Path)
        for path in path_generator:
            print(path)
