import sqlite3
from tabulate import tabulate


def display_neat_table():
    connection = sqlite3.connect('data.db')
    command = connection.cursor()

    command.execute('SELECT * FROM data')
    data = command.fetchall()

    connection.close()
    
    headers = ['IP', 'Status', 'Sus', 'Switches', 'Sus Time', 'Switches Time']
    table = tabulate(data, headers=headers, tablefmt='grid')
    
    return table
