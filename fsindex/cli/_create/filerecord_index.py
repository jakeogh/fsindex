#!/usr/bin/env python3

import click
from kcl.sqlalchemy.self_contained_session import self_contained_session
from kcl.sqlalchemy.model.FileRecord import FileRecord
from kcl.sqlalchemy.BaseMixin import BASE
from kcl.dirops import path_is_dir
from kcl.dirops import all_files_iter
import pathlib
import os

# exists=False or cant pass broken symlinks
# dir_okay=True or cant pass dirs or symlinks to dirs
# resolve_path=False or it will resolve symlinks
@click.command()
@click.argument('paths', type=click.Path(exists=False, dir_okay=True, path_type=bytes, allow_dash=False), nargs=-1)
@click.option('--verbose', is_flag=True)
@click.pass_obj
def filerecord_index(config, paths, verbose):
    for path in paths:
        assert path_is_dir(path)
        with self_contained_session(config.database) as session:
            BASE.metadata.create_all(session.bind)
            pathlib_object = pathlib.Path(os.fsdecode(path))
            for index, path in enumerate(all_files_iter(pathlib_object)):
                filerecord = FileRecord.construct(session=session, path=bytes(path), verbose=verbose)
                session.add(filerecord)
                if index % 100:
                    session.flush()
                    session.commit()
