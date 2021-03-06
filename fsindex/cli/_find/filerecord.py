#!/usr/bin/env python3

import click
from kcl.sqlalchemy.self_contained_session import self_contained_session
from kcl.sqlalchemy.model.FileRecord import FileRecord
from kcl.sqlalchemy.BaseMixin import BASE


# exists=False or cant pass broken symlinks
# dir_okay=True or cant pass dirs or symlinks to dirs
# resolve_path=False or it will resolve symlinks
@click.command()
@click.argument('path', type=click.Path(exists=False, dir_okay=True, path_type=bytes, allow_dash=False), nargs=1)
@click.pass_obj
def filerecord(config, path):
    with self_contained_session(config.database) as session:
        BASE.metadata.create_all(session.bind)
        path, filename = os.path.split(path)
        #session.
        filerecord = FileRecord.construct(session=session, inpath=path)
        filerecord = FileRecord.construct(session=session, inpath=path)
        #session.commit()
        print(bytes(filerecord))
