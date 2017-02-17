#!/usr/bin/env python3

import sys
import os
import sqlite3

conn = sqlite3.connect('/home/user/.fsindex/_good/fsindex.sha1.db')

def search_for_full_path(full_path):
    c = conn.cursor()
    query = '''SELECT * FROM path_db WHERE full_path=?'''
    answer = c.execute(query, (full_path,))
    results = answer.fetchall()
    return results


if __name__ == '__main__':
    full_path = bytes(sys.argv[1], 'UTF8')
    results = search_for_full_path(full_path)
    if len(results) > 0:
        for result in results:
            print(result)
        exit(0)
    exit(1)




#c.execute('''CREATE TABLE path_db (id TEXT, full_path BLOB, file_name BLOB, st_mode INT, st_ino INT, st_dev INT, st_nlink INT, st_uid INT, st_gid INT, st_size INT, st_atime REAL, st_mtime REAL, st_ctime REAL)''')
#c.execute("PRAGMA synchronous = OFF")
