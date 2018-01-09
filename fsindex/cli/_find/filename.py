#!/usr/bin/env python3

import click
import os
from sqlalchemy.sql import text
from kcl.printops import eprint
from kcl.sqlalchemy.self_contained_session import self_contained_session
from kcl.sqlalchemy.model.Filename import Filename


def like_filter(query, name):
    new_query = query.filter(Filename.filename.like(b'%'+name+b'%'))
    return new_query

def ilike_filter_escape(query, name):
    name = name.lower()
    name = name.replace(bytes([92]), bytes([92,92]))
    name = name.decode('utf8') #ugly
    new_query = query.filter(Filename.filename_lower_escape.like('%'+name+'%'))
    return new_query

#def regex_filter(query, name):
#    name = name.lower()
#    new_query = query.filter(text('filename ~ :reg')).params(reg=name)
#    return new_query

@click.command()
@click.option('--like', type=click.Path(exists=False, dir_okay=True, path_type=bytes, allow_dash=False), multiple=True)
@click.option('--ilike', type=click.Path(exists=False, dir_okay=True, path_type=bytes, allow_dash=False), multiple=True)
@click.option('--run', type=click.Path(exists=True, dir_okay=False, path_type=bytes, allow_dash=False), multiple=False, default=False)
#@click.option('--regex', is_flag=True)
@click.pass_obj
def filename(config, like, ilike, run):
    with self_contained_session(config.database, echo=config.database_echo) as session:
        query = session.query(Filename)
        for name in like:
            query = like_filter(query, name)
        for name in ilike:
            query = ilike_filter_escape(query, name)
        #elif regex:  # broken for bytes
        #    query = session.query(Filename).filter(text('filename ~ :reg')).params(reg=name)
        #else:
        #    assert len(names) == 1
        #    query = session.query(Filename).filter(Filename.filename == names[0])

        for filename in query:
            #print(filename)
            for item in filename.filerecords:
                print(item.file)
                if run:
                    command = run + b'' + item.name
                    os.system(command)

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

# bytes(session.execute("SELECT filename FROM filename WHERE encode(filename, 'escape') ILIKE encode('%JaguarAJ-V8Engine%'::bytea, 'escape')").scalar())


