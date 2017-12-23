#!/usr/bin/env python3
import sqlite3

def get_db_connection(database_file='/poolz3_8x5TB_A/__fsindex/_good/fsindex.sha1.db'):
    #conn = sqlite3.connect('/poolz3_8x5TB_A/__fsindex/_good/fsindex.sha1.db')
    conn = sqlite3.connect(database_file)
    c = conn.cursor()
    return c
