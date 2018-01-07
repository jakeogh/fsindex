#!/usr/bin/env python3

from fsindex.test.test_enviroment import *
with self_contained_session(CONFIG.database_timestamp) as session:
    BASE.metadata.create_all(session.bind)

    path = Path.construct(session=session, path=b"/level1")
    session.add(path)
    session.commit()

    path_duplicate = Path.construct(session=session, path=b"/level1")
    session.add(path_duplicate)
    session.commit()

    assert path.id == path_duplicate.id
    assert id(path) == id(path_duplicate)

db_result = [('select COUNT(*) from filename;', 2),
             ('select COUNT(*) from path;', 1),
             ('select COUNT(*) from pathfilename;', 2)]

check_db_result(config=CONFIG, db_result=db_result)
