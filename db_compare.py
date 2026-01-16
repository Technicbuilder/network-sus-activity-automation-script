import time
import sqlite3
from pathlib import Path
from network_scan import scan_network
from database import store
#    FILE MUST BE RAN BEFORE USING DATABASE.py

#   every 10 mins, the program should ping all devices, if some do not respond, add 1 to sus_count

#   create database/establish connection

# implement in a function with while true in it LATER// time.sleep(600) # program will execute every 10 minutes

file_path = Path(__file__).parent / 'network_data.db'
file_exists = file_path.exists()    #   verify database file existance

conn = sqlite3.connect(str(file_path))
command = conn.cursor()

results = scan_network()    #   results now stores dictionary result {host:host.status}

command.execute('SELECT IP, STATUS FROM data')
data = command.fetchall()
# Output: [('192.168.1.1', 'up'), ('10.0.0.5', 'down')]

#   use a dictionary to prevent double nested for loop (prevent O(n**2) i think)
known_ips = {}
known_ips.update([output for output in data]) # appends to dictionary

new_ip = known_ips - results    #   new ips obtained
store(new_ip)   #   need to implement sus counter

