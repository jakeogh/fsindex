#!/usr/bin/env python3

import sys
import os
import hashlib
from collections import OrderedDict
from .db_connection import get_db_connection()
c = get_db_connection()

FIELDS = OrderedDict((
    ('path_hash','TEXT'),
    ('full_path','BLOB'),
    ('file_name','BLOB'),
    ('data_hash','TEXT'),
    ('st_mode','INT'),
    ('st_ino','INT'),
    ('st_dev','INT'),
    ('st_nlink','INT'),
    ('st_uid','INT'),
    ('st_gid','INT'),
    ('st_size','INT'),
    ('st_atime_ns','INT'),
    ('st_mtime_ns','INT'),
    ('st_ctime_ns','INT'),
    ('existance_timestamp', 'INT'),
    ('nonexistance_timestamp', 'INT')
    ))

    # stuff to add:
    #   indexing timestamp
    #   file extended attrs
    #   sha256/512/whirpool
    #
    #   type str?

MODE_DESCRIPTIONS = OrderedDict((
    ('S_IFSOCK', 'Socket'),         #49152
    ('S_IFLNK', 'Symbolic link'),   #40960
    ('S_IFREG', 'Regular file'),    #32768
    ('S_IFBLK', 'Block device'),    #24576
    ('S_IFDIR', 'Directory'),       #16384
    ('S_IFCHR', 'Character device'),#8192
    ('S_IFIFO', 'FIFO')             #4096
    ))

MODE_FUNCTIONS = OrderedDict((
    ('S_ISDIR', 'directory'),
    ('S_ISCHR', 'character special device file'),
    ('S_ISBLK', 'block special device file'),
    ('S_ISREG', 'regular file'),
    ('S_ISFIFO', 'FIFO (named pipe)'),
    ('S_ISLNK', 'symbolic link'),
    ('S_ISSOCK', 'socket'),
    ('S_ISDOOR', 'door'),
    ('S_ISPORT', 'event port'),
    ('S_ISWHT', 'whiteout')
    ))

field_str = ''
for label in FIELDS.keys():
    #print(label)
    labeltype = FIELDS[label]
    field_str = field_str + label + ' ' + labeltype + ', '

def sqlite_create_database():
    query = '''CREATE TABLE path_db (''' + field_str + '''PRIMARY KEY)'''
    c.execute(query) #bug there should not be a requirement to be unique, a file could change.
    c.execute("PRAGMA synchronous = OFF")

def db_stats():
    query = '''SELECT Count(*) FROM path_db'''
    answer = c.execute(query)
    return answer.fetchall()

