import os
import platform


import psutil

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def validate_port(port_number):
    try:
        port_number = int(port_number)
    except ValueError:
        raise ValueError(f"{port_number} is not a valid port number")

    if not (0 <= port_number <= 65535):
        raise ValueError(f"Port {port_number} is out of valid range ( 0 - 65535 )")
    return port_number


def debug_resources():
    proc = psutil.Process(os.getpid())
    mem = proc.memory_info().rss / (1024 ** 2)
    print(f"Memory Usage: {mem:.2f} MB")
    print(f"Threads: {proc.num_threads()}")
    print(f"Open Files: {len(proc.open_files())}")
