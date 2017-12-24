#!/usr/bin/env python3

import click
from kcl.sqlalchemy.self_contained_session import self_contained_session
from kcl.sqlalchemy.model.FileRecord import FileRecord
from kcl.sqlalchemy.BaseMixin import BASE

@click.command()
@click.argument('path', type=click.Path(exists=True, dir_okay=False, path_type=bytes, allow_dash=False), nargs=1)
@click.pass_obj
def filerecord(config, path):
    with self_contained_session(config.database) as session:
        BASE.metadata.create_all(session.bind)
        filerecord = FileRecord.construct(session=session, inpath=path)
        session.commit()
        print(filerecord)
