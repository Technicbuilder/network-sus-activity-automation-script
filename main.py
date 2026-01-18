#   this will be the main file where everything is executed, should look clean
#   this will do the inital scan

from database import *
from data_compare import compare
from scan_network import scan
import threading
from discord_alert import run_bot
import time

def main():
        #   runs bot in the background
    bot_thread = threading.Thread(target = run_bot, daemon = True)
    bot_thread.start()
    
    #   time to allow bot to boot
    time.sleep(7)
    
    create_table()
    initial_scan = scan()
    update(initial_scan, is_initial = True)
    
    while True:
        time.sleep(600) #   10mins between scans
        consistent_scan = scan()
        result = compare(consistent_scan)
        update(result, is_initial = False)
        delete_old_and_inactive()
    
if __name__ == "__main__":
    main() 