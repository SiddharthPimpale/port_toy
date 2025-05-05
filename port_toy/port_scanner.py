import socket
import gc

from colorama import Fore
import psutil

from port_toy.utils import validate_port


def check_port(port, host="127.0.0.1"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        result = sock.connect_ex((host, port))
        return result == 0

def get_process_from_port(port):
    for connection in psutil.net_connections(kind="inet"):
        if connection.laddr.port == port:
            process_id = connection.pid
            if process_id:
                try:
                    process = psutil.Process(process_id)
                    return process_id, process.name()
                except psutil.NoSuchProcess:
                    pass
    return None, None

#  this can also be used to scan a remote host
#  feature to be added, just need to take host as input and we can pass it in the check_port method
def scan_port():
    port = validate_port(input("Enter port number to scan:"))
    if check_port(port):
        print(f"[+] Port {port} is OPEN.")
        process_id, process_name = get_process_from_port(port)
        if process_id:
            print(f"    PID: {process_id}, Name: {process_name}")
        else:
            print(f"    process info not found.")
    else:
        print(f"[-] Port: {port} is CLOSED.")


def scan_by_process_name(filter_name):
    matched = []
    print(Fore.GREEN + "Listing all open ports ...")
    try:
        connections = psutil.net_connections(kind="inet")
    except Exception as ex:
        print(Fore.RED + f"Error fetching connections: {ex}")
        return
    for conn in connections:
        process_id = conn.pid
        if not process_id:
            continue
        try:
            current_process = psutil.Process(process_id)
            process_name = current_process.name()

            if filter_name.lower() in process_name.lower():
                matched.append((conn.laddr.port, process_id, process_name))
        except psutil.NoSuchProcess:
            continue

    if not matched:
        if filter_name:
            print(Fore.YELLOW + f"No open ports found with this name: {filter_name}")
        else:
            print(Fore.YELLOW + "No open ports found.")
    else:
        heading = f"Open ports matching process name '{filter_name}':" if filter_name else "All open ports:"
        print(Fore.CYAN + heading)
        for port, process_id, process_name in sorted(set(matched)):
            print(f"[+] Port {port} -- PID {process_id} -- Name: {process_name}")

def list_open_ports():
    print(Fore.GREEN + "Listing all open ports ...")
    try:
        connections = psutil.net_connections(kind="inet")
    except Exception as ex:
        print( Fore.RED +f"Error fetching connections: {ex}")
        return
    checked = set()
    for conn in connections:
        laddr = conn.laddr
        if laddr and laddr.port not in checked:
            checked.add(laddr.port)
            process_id = conn.pid
            try:
                process_name = psutil.Process(process_id).name() if process_id else "-"
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process_name="-"
            print(f"[+] Port {laddr.port} PID: {process_id or '-'} Name:{process_name}")
    gc.collect()