#   This code is for the database
#   1. The code will create a database table if one is not already created
#   2. It will store data from the inital scan, then update the table for new devices
#   3. New devices have sus incremented (new ips are kinda sus, not everyday you get a new device, unless when you have guests around or something) ill make it to reset after 24-48hrs later

import sqlite3
from datetime import datetime, timedelta
import asyncio
from discord_alert import send_alert, bot
def create_table():
    connection = sqlite3.connect('data.db')
    command = connection.cursor()
    
    command.execute('''
                    CREATE TABLE IF NOT EXISTS data (
                        ip TEXT NOT NULL PRIMARY KEY,
                        active BOOLEAN,
                        sus INTEGER,
                        switches INTEGER,
                        sus_time TEXT,
                        switches_time TEXT
                        
                    )
                    ''')
    
    connection.commit()
    connection.close()
    

def update(initial_scan, is_initial = False):
    connection = sqlite3.connect('data.db')
    command = connection.cursor()
    
    for host, status in initial_scan.items():
        command.execute('SELECT active, sus, switches, sus_time, switches_time FROM data WHERE ip = ?', (host,))  # FIXED - added sus_time, switches_time to SELECT
        result = command.fetchone()
        
        if result:
            old_status, sus, switches, sus_time, switches_time = result
            
            if sus_time:
                last_sus_time = datetime.fromisoformat(sus_time)
                if datetime.now() - last_sus_time > timedelta(hours=48):
                    sus = 0
                    sus_time = None
            if sus >= 5:
                    asyncio.run_coroutine_threadsafe(
                    send_alert(f'Suspicious activity: {host}, LV: {sus}'),
                    bot.loop
                    )   #   trigger discord bot to send info
                    
            if old_status != status:
                switches += 1
                switches_time = datetime.now().isoformat()
                if switches >= 3:
                    asyncio.run_coroutine_threadsafe(
                    send_alert(f"⚠️ Frequent changes: {host} (switches={switches})"),
                    bot.loop
                    )
                    switches = 0
            command.execute('UPDATE data SET active = ?, switches = ?, sus = ?, sus_time = ?, switches_time = ? WHERE ip = ?', (status, switches, sus, sus_time, switches_time, host))  # FIXED - changed sus_timestamp/switches_timestamp to sus_time/switches_time
        else:
            sus_value = 0 if is_initial else 1
            sus_ts = datetime.now().isoformat() if sus_value == 1 else None
            command.execute('INSERT INTO data (ip, active, sus, switches, sus_time, switches_time) VALUES (?, ?, ?, ?, ?, ?)', (host, status, sus_value, 0, sus_ts, None))  # FIXED - changed sus_timestamp/switches_timestamp to sus_time/switches_time
    
    connection.commit()
    connection.close()
    
#   got too lazy to write this code so i got claude to do this function for me, my brain is kinda fried rn, been doing this for a few hours atp - learning how to use sqlite3
def delete_old_and_inactive():
    connection = sqlite3.connect('data.db')
    command = connection.cursor()
    
    command.execute('SELECT ip, switches_time FROM data WHERE active = 0 OR active = "down"')  # FIXED - changed switches_timestamp to switches_time
    results = command.fetchall()
    
    for ip, timestamp in results:
        if timestamp:
            last_change = datetime.fromisoformat(timestamp)
            if datetime.now() - last_change > timedelta(hours=120):
                command.execute('DELETE FROM data WHERE ip = ?', (ip,))
    
    connection.commit()
    connection.close()