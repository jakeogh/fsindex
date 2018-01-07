#!/usr/bin/env python3

from fsindex.test.test_enviroment import *
with self_contained_session(CONFIG.database_timestamp) as session:
    BASE.metadata.create_all(session.bind)

    path = Path.construct(session=session, path=b"/")
    session.add(path)
    session.commit()

db_result = [('select COUNT(*) from filename;', 1),
             ('select COUNT(*) from path;', 1),
             ('select COUNT(*) from pathfilename;', 2)]

check_db_result(config=CONFIG, db_result=db_result)
