import psutil

from port_toy.port_scanner import check_port, get_process_from_port


def kill_process(process_id):
    try:
        process = psutil.Process(process_id)
        process.terminate()
        process.wait(timeout=3)
        return True
    except Exception as ex:
        print(f"Error: {ex}")
        return False


def kill_ports():
    port = int(input("Enter port number to kill process on:"))
    if check_port(port):
        process_id, process_name = get_process_from_port(port)
        if process_id:
            confirm_kill = input(f"Found PID: {process_id} ({process_name}). kill it? [y,N]:").lower()
            if confirm_kill == 'y':
                if kill_process(process_id):
                    print(f"✔ Killed process {process_id}")
                else:
                    print(f"✘ Failed to kill process {process_id}")
            else:
                print("[-] Process kill abort")
        else:
            print("[-] No process found")
    else:
        print(f"Port {port} not in use.")