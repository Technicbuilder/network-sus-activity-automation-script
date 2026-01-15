import sqlite3
from pathlib import Path
from tabulate import tabulate

#   create database/establish connection
file_path = Path(__file__).parent / 'network_data.db'
file_exists = file_path.exists()    #   verify database file existance

conn = sqlite3.connect(str(file_path))
command = conn.cursor()

#   creates table after verifying non-existence
if not file_exists:
    command.execute('''
                CREATE TABLE data(
                    IP TEXT NOT NULL PRIMARY KEY,
                    STATUS TEXT,
                    SUS_COUNT INTEGER,
                    IP_SWITCHES INTEGER);
                ''')

#   add in data from network scan {host:host.status}

def store(results):
    for host, status in results.items():
        command.execute('INSERT INTO data (IP, STATUS) VALUES (?, ?)', (host, status))
    
    conn.commit()
    command.execute('SELECT * FROM data')
    
    rows = command.fetchall()
    headers = [description[0] for description in command.description]
    print(tabulate(rows, headers=headers, tablefmt='grid'))
