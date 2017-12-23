#!/usr/bin/env python3

import click
from filerecorddb.model.Iri import Iri
from kcl.sqlalchemy.self_contained_session import self_contained_session

@click.command()
@click.pass_obj
def list_filerecords(config):
    with self_contained_session(config.database) as session:
        filerecord_generator = session.query(Iri)
        for filerecord in filerecord_generator:
            print(filerecord)
