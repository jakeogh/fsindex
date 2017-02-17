#!/usr/bin/env python3

import sys
import os
from .db_connection import c

def search_for_full_path(full_path):
    #c = conn.cursor()
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


