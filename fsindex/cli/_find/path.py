#!/usr/bin/env python3

import click
from sqlalchemy.sql import text
from kcl.printops import eprint
from kcl.sqlalchemy.self_contained_session import self_contained_session
from kcl.sqlalchemy.model.Path import Path

@click.command()
@click.argument('path', type=click.Path(exists=False, dir_okay=True, path_type=bytes, allow_dash=False), nargs=1)
@click.option('--like', is_flag=True)
@click.option('--regex', is_flag=True)
@click.pass_obj
def path(config, path, like, regex):
    with self_contained_session(config.database, echo=config.database_echo) as session:
        if like and regex:
            eprint("--like and --regex are mutually exclusive.")
            quit(1)
        if like:
            path_generator = session.query(Path).filter(Path.path.like(b'%'+path+b'%'))
        elif regex:
            path_generator = session.query(Path).filter(text('path ~ :reg')).params(reg=path)
        else:
            path_generator = session.query(Path).filter(Path.path == path)

        for path in path_generator:
            #print(path)
            for item in path.filerecords:
                print(item)

# bytes(session.execute("SELECT filename FROM filename WHERE filename = 'JaguarAJ-V8Engine.pdf'::bytea").fetchall()[0][0])
# b'JaguarAJ-V8Engine.pdf'

# bytes(session.execute("SELECT filename FROM filename WHERE filename = 'JaguarAJ-V8Engine.pdf'::bytea").fetchone()[0])
# b'JaguarAJ-V8Engine.pdf'

# from kcl.sqlalchemy.model.Path import Path
# In [10]: session.query(Path).filter(Path.filename == b'JaguarAJ-V8Engine.pdf').one()
#2017-12-30 01:32:42,137 INFO sqlalchemy.engine.base.Engine SELECT filename.id AS filename_id, filename.filename AS filename_filename
# FROM filename
# WHERE filename.filename = %(filename_1)s
# 2017-12-30 01:32:42,137 INFO sqlalchemy.engine.base.Engine {'filename_1': <psycopg2.extensions.Binary object at 0x7fd7bf079f30>}
# Out[10]: b'JaguarAJ-V8Engine.pdf'


# bytes(session.execute("SELECT filename FROM filename WHERE filename = 'JaguarAJ-V8Engine.pdf'::bytea").scalar())


