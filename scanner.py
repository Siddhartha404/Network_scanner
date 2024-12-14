from ping3 import ping
import socket
import concurrent.futures
import ipaddress
import time

def ping_host(host):
    """
    Ping a host and return its status and latency
    """
    try:
        response = ping(host, timeout=1)
        if response is not None:
            return f"{host} is up (Latency: {response:.2f} ms)"
        else:
            return f"{host} is not reachable"
    except Exception as e:
        return f"Error pinging {host}: {e}"

def check_port(host, port):
    """
    Check if a specific port is open on a host
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            return result == 0
    except Exception:
        return False

def scan_ports(host, port_range=(1, 1024), max_threads=50):
    """
    Scan a range of ports on a host using concurrent threads
    """
    open_ports = []
    start_port, end_port = port_range

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        port_futures = {
            executor.submit(check_port, host, port): port 
            for port in range(start_port, end_port + 1)
        }

        for future in concurrent.futures.as_completed(port_futures):
            port = port_futures[future]
            if future.result():
                open_ports.append(port)
                print(f"Port {port} is open")

    return sorted(open_ports)

def scan_network(target, max_threads=50):
    """
    Perform a comprehensive network scan
    """
    try:
        # Validate and get IP addresses
        ip_network = ipaddress.ip_network(target, strict=False)
        ip_addresses = list(ip_network.hosts())
    except ValueError:
        print(f"Invalid IP address or network: {target}")
        return

    start_time = time.time()
    print(f"Scanning network: {target}")
    print(f"Total IPs to scan: {len(ip_addresses)}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        ping_futures = {
            executor.submit(ping_host, str(ip)): ip 
            for ip in ip_addresses
        }

        active_hosts = []
        for future in concurrent.futures.as_completed(ping_futures):
            ip = ping_futures[future]
            result = future.result()
            if "is up" in result:
                print(result)
                active_hosts.append(str(ip))
                
        print("\nScanning open ports on active hosts...")
        for host in active_hosts:
            print(f"\nScanning {host}:")
            open_ports = scan_ports(host)
            print(f"Open ports on {host}: {open_ports}")

    end_time = time.time()
    print(f"\nScan completed in {end_time - start_time:.2f} seconds")

def main_menu():
    while True:
        print("\n--- Network Scanner ---")
        print("1. Ping a Host")
        print("2. Scan Ports on a Host")
        print("3. Scan Entire Network")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            host = input("Enter host to ping (IP or hostname): ")
            print(ping_host(host))
        
        elif choice == '2':
            host = input("Enter host to scan (IP or hostname): ")
            scan_type = input("Scan all ports or specific port? (all/specific): ").lower()
            
            if scan_type == 'all':
                scan_ports(host)
            elif scan_type == 'specific':
                port = int(input("Enter port number to scan: "))
                result = check_port(host, port)
                print(f"Port {port} is {'open' if result else 'closed'}")
        
        elif choice == '3':
            target = input("Enter network to scan (e.g., 192.168.1.0/24): ")
            scan_network(target)
        
        elif choice == '4':
            print("Exiting Network Scanner. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()