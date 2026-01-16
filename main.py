import time
from network_scan import scan_network
from database import store

def main():
    initial_scan_result = scan_network()
    store(results=initial_scan_result)
    # after storing intitial results, we must run another network scan 10 minutes
    # then compare results to check for new ips or document any suspicious activity
    while True:
        time.sleep(600)
        scan_result = scan_network()


if __name__ == "__main__":
    main()
