from network_scan import scan_network
from database import store
from tabulate import tabulate

scan_result = scan_network()

store(results=scan_result)