import nmap

def scan_network():
    
    scanner = nmap.PortScanner() #   initialise nmap object
    network_cidr = '192.168.0.1/24' #   cidr is an ip allocation method
    scanner.scan(hosts=network_cidr, arguments='-sn') #   -sn just pings hosts
    
    return {host:scanner[host].state() for host in scanner.all_hosts()} #   returns as a dictionary {host:host.statues}
    
    # returns dictionary with values, e.g.:
    # {host:host.status, host:host.status, host:host.status ....}
