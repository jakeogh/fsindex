#!/usr/bin/env python3

import sqlite3
#print("sqlite3.connect()")
conn = sqlite3.connect('/poolz3_8x5TB_A/__fsindex/_good/fsindex.sha1.db')
#print("conn.cursor()")
c = conn.cursor()
