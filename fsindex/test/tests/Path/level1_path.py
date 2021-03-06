#!/usr/bin/env python3

from fsindex.test.test_enviroment import *
with self_contained_session(CONFIG.database_timestamp) as session:
    BASE.metadata.create_all(session.bind)

    path = Path.construct(session=session, path=b"/level1")
    session.add(path)
    session.commit()

db_result = [('select COUNT(*) from filename;', 2),
             ('select COUNT(*) from path;', 2)]

check_db_result(config=CONFIG, db_result=db_result)
