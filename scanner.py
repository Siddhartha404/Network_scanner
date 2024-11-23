from ping3 import ping
import socket

def pingHost(host):
    responce = ping(host)
    if responce:
        return f"{host} is up with {responce} latency"
    else:
        return f"{host} is not rechable"

def scan_port(host,port=None):
    if port is None:
        print(f"ScaSnning on all ports on {host}")
        openPorts = []
        for ports in range(1,1025):
            if check_port(host, ports):
                openPorts.append(ports)
        print(openPorts)
        return openPorts
    else:
        return check_port(host,port)
    
def check_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.05)

    result = sock.connect_ex((host,port))
    sock.close
    if result == 0:
        print(f"Port {port} is open")
        return True
    
    return False


