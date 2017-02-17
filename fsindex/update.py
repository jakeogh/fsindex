#!/usr/bin/env python3

#fsindex poc
#Public Domain - jak

import sys
import os
import hashlib
from fsindex_search_for_full_path import search_for_full_path
#import stat
from stat import *
from kcl.fileops import is_regular_file
from kcl.dirops import path_is_dir
from kcl.hashops import sha1_hash_file
from kcl.dirops import all_files

from .dbconnection import c


def update_db(path):
    assert path.startswith(b'/')

    if path_is_dir(path):
        print("indexing folder:", path, file=sys.stderr)
        print("generating all_paths:", file=sys.stderr)
        #all_paths = [os.path.join(path, filename) for path, dirs, files in os.walk(path) for filename in files]
        all_paths = all_files(path)
        print("done generating all_paths:", file=sys.stderr)

    else:
        os._exit(1)

    skipped_file_list = []

    for index, path in enumerate(all_paths):
#       print("path:", path)
        existing_db_entrys = search_for_full_path(path)
        if len(existing_db_entrys) > 0:
#           print("exists in db, skipping")
            continue

        path_hash = hashlib.sha1(path).hexdigest()
        file_name = path.split(b'/')[-1]
        try:
            stat = os.stat(path)
        except:
            print("error doing stat() on %s, skipping.", path)
            continue

        if is_regular_file(path):
            if stat.st_size == 0:
                continue
            if stat.st_size >= 1024*1024*1024: #1GB
                if stat.st_size >= 1024*1024*1024*1024: #1TB
                    print("skipping file >=1TB", path)
                    skipped_file_list.append(path)
                    continue
                print("hashing file >1GB:", path, str(stat.st_size/1024.0/1024.0/1024.0)+'GB')

            try:
                data_hash = sha1_hash_file(path)
            except:
                print("error hashing file:", path, "skipping.")
                continue
        else:   #not a reg file
            continue

        row_to_insert = (path_hash, path, file_name, data_hash, stat.st_mode, stat.st_ino, stat.st_dev, stat.st_nlink, stat.st_uid, stat.st_gid, stat.st_size, stat.st_atime, stat.st_mtime, stat.st_ctime)
        c.execute("INSERT INTO path_db VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row_to_insert)
        print(index, row_to_insert, file=sys.stderr)
        conn.commit()

    if len(skipped_file_list) > 0:
        print("skipped_file_list:", skipped_file_list, file=sys.stderr)


if __name__ == '__main__':

    path = bytes(sys.argv[1], 'UTF-8')
    path = os.path.realpath(path)
    update_db(path)
