#   this file will scan the nework using the scan function from scan_network file
#   it will compare what it scanned to initial results, increment sus or switches depending on activity

import sqlite3
from scan_network import scan


def original_data():
    connection = sqlite3.connect('data.db')
    command = connection.cursor()

    command.execute('SELECT * FROM data')
    original_data = command.fetchall()
    
    connection.close()
    
    dict_original_data = {x[0]: x[1] for x in original_data}

    return dict_original_data


def compare(consistent_scan, initial_data = None):
    #   subtracts current data from old data, returning the result
    #   result is updated in database.py from main.py
    if initial_data is None:
        initial_data = original_data()
    
    new_entries = set(consistent_scan.keys()) - set(initial_data.keys())
    
    #   nmap scan returns {host: host.status} therefore we need the same data here
    #   otherwise dictionaries cannot be subtracted
    new_entries_dict = {key: consistent_scan[key] for key in new_entries}
    
    print(new_entries_dict)
    return new_entries_dict