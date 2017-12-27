#!/usr/bin/env python3

import click
from kcl.sqlalchemy.self_contained_session import self_contained_session
from kcl.sqlalchemy.model.FileRecord import FileRecord
from kcl.sqlalchemy.BaseMixin import BASE
from kcl.dirops import path_is_dir
from kcl.dirops import all_files

# exists=False or cant pass broken symlinks
# dir_okay=True or cant pass dirs or symlinks to dirs
# resolve_path=False or it will resolve symlinks
@click.command()
@click.argument('path', type=click.Path(exists=False, dir_okay=True, path_type=bytes, allow_dash=False), nargs=1)
@click.pass_obj
def filerecord_index(config, path):
    assert path_is_dir(path)
    with self_contained_session(config.database) as session:
        BASE.metadata.create_all(session.bind)
        for index, inpath in enumerate(all_files(path)):
            filerecord = FileRecord.construct(session=session, inpath=inpath)
            session.add(filerecord)
            #if index % 1000:
            session.flush()
            session.commit()
        #print(bytes(filerecord))
