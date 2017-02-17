#!/usr/bin/env python3

import sys
import os
import hashlib
import pprint
import sqlite3

from fsindex_update import update_db

pp = pprint.PrettyPrinter(indent=4)
conn = sqlite3.connect('/home/user/.fsindex/_good/fsindex.sha1.db')
c = conn.cursor()

def file_exists(file):
#   print("(checking) file_exists()", file)
    if os.path.isfile(file):    #unlike os.path.exists(False), os.path.isfile(False) returns False so no need to call path_exists() first.
        return True
    return False


def folder_exists(path):
    if os.path.isdir(path):     #unlike os.path.exists(False), os.path.isdir(False) returns False so no need to call path_exists() first.
        return True
    return False


def get_data_hash_for_file_path(file):
    if not file_exists(file):
        return False

    file_hash = b''
    query = '''SELECT data_hash FROM path_db WHERE full_path=?'''
    full_path_search_results = c.execute(query, (file,))

    try:
        file_hash = full_path_search_results.fetchone()[0]
    except:
        pass

    if len(file_hash) > 0:
        return file_hash
    else:
        print("found file not in database:", file)
        print("this should not happen, exiting")
        exit(1)
#       print("manually hashing file:", file)
#       with open(file, 'rb') as fh:
#           file_hash = hashlib.sha1(fh.read()).hexdigest()

    return file_hash


def search_for_duplicate_data_hashes(data_hash):
    query = '''SELECT full_path FROM path_db WHERE data_hash=?'''
    hash_match = c.execute(query, (data_hash,))
    results = hash_match.fetchall()
    final_results = []

    for result in results:
        final_results.append(result[0])

    return final_results


def prune_results_outside_path(results, path):
    pruned_results = []
    for result in results:
        if path in result:
            pruned_results.append(result)

    return pruned_results


def generate_match_dict(path):
    update_db(path) #critical step or files could be skipped/missed. todo: use inotify
#   print("done calling update_db()")
    hash_match_dict = {}

    if folder_exists(path):
#       print("indexing folder")
        all_paths = [os.path.join(path, filename) for path, dirs, files in os.walk(path) for filename in files]

        for file in all_paths:
#           print("\nfile:",file)
            if file_exists(file):   #weed out folders
                if path in file: #dont look for matches outside given path (os.walk might have followed a symlink somewhere)
                    file_data_hash = get_data_hash_for_file_path(file)
                    duplicate_data_hash_results = prune_results_outside_path(search_for_duplicate_data_hashes(file_data_hash), path)

#                   print("(before dedupe) duplicate_data_hash_results:", duplicate_data_hash_results)
#                   print("(before dedupe) len(duplicate_data_hash_results):", len(duplicate_data_hash_results))
            
                    existing_duplicate_data_hash_results = []
                    for dup_file in duplicate_data_hash_results:
#                       print("checking if dup_file exists:", dup_file)
                        if file_exists(dup_file):
                            existing_duplicate_data_hash_results.append(dup_file)
                            
                                
                    if len(existing_duplicate_data_hash_results) > 1:
#                       print("(after dedupe) duplicate_data_hash_results:", existing_duplicate_data_hash_results)
#                       print(existing_duplicate_data_hash_results)
                        
                        hash_match_dict[file_data_hash] = set([])

                        for duplicate_file in existing_duplicate_data_hash_results:
#                           if file_exists(duplicate_file):
                            hash_match_dict[file_data_hash].add(duplicate_file)

    return hash_match_dict


if __name__ == '__main__':
    path = bytes(sys.argv[1], 'UTF8')   #bug, not all valid paths are valid UTF8
    path = os.path.realpath(path)

    hash_match_dict = generate_match_dict(path)

    for hash in hash_match_dict.keys():
        print(hash+':')
        pp.pprint(hash_match_dict[hash])
