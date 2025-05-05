# external package imports
from colorama import Fore

# project imports
from port_toy.banner import print_banner
from port_toy.port_scanner import scan_port, scan_by_process_name
from port_toy.process_manager import kill_ports
from port_toy.utils import clear_screen, debug_resources

def main():
    while True:
        try:
            clear_screen()
            print_banner()
            print("""
            ====================================
                  PortToy - Dev Utility
            ====================================
            1. Scan a specific port
            2. Scan by process name
            3. List all open ports
            4. Kill process on a port
            5. Exit
            """)
            choice = input("Enter your choice:")
            if choice == "1":
                scan_port()
            elif choice == "2":
                scan_by_process_name(input("Enter process name:"))
            elif choice == "3":
                scan_by_process_name("")
            elif choice == "4":
                kill_ports()
            elif choice == "5":
                print("Bye ...")
                break
            elif choice == "9":
                debug_resources()
            else:
                print("Invalid option")
        except KeyboardInterrupt:
            print(Fore.BLUE + f"Exiting ...")
            break
        except Exception as ex:
            print(Fore.RED + f"An Error occured: {ex}")
        input("\n Press enter to return to menu")

if __name__ == '__main__':
    main()
