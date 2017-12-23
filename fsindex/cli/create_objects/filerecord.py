#!/usr/bin/env python3

import click
from kcl.sqlalchemy.self_contained_session import self_contained_session
from kcl.sqlalchemy.model.FileRecord import FileRecord
from kcl.sqlalchemy.BaseMixin import BASE

@click.command()
@click.argument('path', required=True, nargs=1)
@click.pass_obj
def filerecord(config, path):
    with self_contained_session(config.database) as session:
        #BASE.metadata.create_all(session.bind)
        filerecord = FileRecord.construct(inpath=path)
        session.commit()
        print(filerecord)