#   this will be the main file where everything is executed, should look clean
#   this will do the inital scan

from database import *
from data_compare import compare
from scan_network import scan


def main():
    create_table()
    initial_scan = scan()
    update(initial_scan, is_initial = True)
    
    while True:
        consistent_scan = scan()
        result = compare(consistent_scan)
        update(result, is_initial = False)
        delete_old_and_inactive()
        break
    
main()