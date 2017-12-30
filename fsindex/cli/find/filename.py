#!/usr/bin/env python3

import click
from kcl.sqlalchemy.self_contained_session import self_contained_session
from kcl.sqlalchemy.model.Filename import Filename

@click.command()
@click.argument('name', type=click.Path(exists=False, dir_okay=True, path_type=bytes, allow_dash=False), nargs=1)
@click.option('--like', is_flag=True)
@click.pass_obj
def filename(config, name, like):
    with self_contained_session(config.database) as session:
        #filename_generator = session.query(Filename).filter(Filename.filename == b'JaguarAJ-V8Engine.pdf')
        if like:
            filename_generator = session.query(Filename).filter(Filename.filename.like('%'+name+'%'))
        else:
            filename_generator = session.query(Filename).filter(Filename.filename == name)
        for filename in filename_generator:
            print(filename)

# bytes(session.execute("SELECT filename FROM filename WHERE filename = 'JaguarAJ-V8Engine.pdf'::bytea").fetchall()[0][0])
# b'JaguarAJ-V8Engine.pdf'

# bytes(session.execute("SELECT filename FROM filename WHERE filename = 'JaguarAJ-V8Engine.pdf'::bytea").fetchone()[0])
# b'JaguarAJ-V8Engine.pdf'

# from kcl.sqlalchemy.model.Filename import Filename
# In [10]: session.query(Filename).filter(Filename.filename == b'JaguarAJ-V8Engine.pdf').one()
#2017-12-30 01:32:42,137 INFO sqlalchemy.engine.base.Engine SELECT filename.id AS filename_id, filename.filename AS filename_filename
# FROM filename
# WHERE filename.filename = %(filename_1)s
# 2017-12-30 01:32:42,137 INFO sqlalchemy.engine.base.Engine {'filename_1': <psycopg2.extensions.Binary object at 0x7fd7bf079f30>}
# Out[10]: b'JaguarAJ-V8Engine.pdf'


# bytes(session.execute("SELECT filename FROM filename WHERE filename = 'JaguarAJ-V8Engine.pdf'::bytea").scalar())


