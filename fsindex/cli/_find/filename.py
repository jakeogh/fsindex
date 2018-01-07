#!/usr/bin/env python3

import click
from sqlalchemy.sql import text
from kcl.printops import eprint
from kcl.sqlalchemy.self_contained_session import self_contained_session
from kcl.sqlalchemy.model.Filename import Filename


def like_filter(query, name):
    new_query = query.filter(Filename.filename.like(b'%'+name+b'%'))
    return new_query

def ilike_filter(query, name):
    new_query = query.filter(Filename.filename.ilike(b'%'+name+b'%'))
    return new_query

@click.command()
#@click.argument('names', type=click.Path(exists=False, dir_okay=True, path_type=bytes, allow_dash=False), nargs=-1)
@click.option('--like', type=click.Path(exists=False, dir_okay=True, path_type=bytes, allow_dash=False), nargs=-1)
@click.option('--ilike', is_flag=True)
@click.option('--regex', is_flag=True)
@click.pass_obj
def filename(config, like, ilike, regex):
    with self_contained_session(config.database, echo=config.database_echo) as session:
        if like and regex:
            eprint("--like and --regex are mutually exclusive.")
            quit(1)
        if ilike and regex:
            eprint("--ilike and --regex are mutually exclusive.")
            quit(1)
        if like and ilike:
            eprint("--like and --ilike are mutually exclusive.")
            quit(1)
        query = session.query(Filename)
        for name in like:
            query = like_filter(query, name)
        for name in ilike:
            query = ilike_filter(query, name)
        #elif regex:  # broken for bytes
        #    query = session.query(Filename).filter(text('filename ~ :reg')).params(reg=name)
        #else:
        #    assert len(names) == 1
        #    query = session.query(Filename).filter(Filename.filename == names[0])

        for filename in query:
            #print(filename)
            for item in filename.filerecords:
                print(item)

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


