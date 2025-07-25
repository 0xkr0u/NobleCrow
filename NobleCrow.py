import socket
import sys
import threading
from queue import Queue

# --- Configuration ---
# Default target host (localhost for safety)
DEFAULT_HOST = '127.0.0.1'
# Default port range (common service ports)
DEFAULT_START_PORT = 1
# Changed to the maximum possible port number as requested
DEFAULT_END_PORT = 65535
# Default connection timeout in seconds
DEFAULT_TIMEOUT = 1

# --- ANSI Color Codes ---
# Define color codes for terminal output
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_CYAN = "\033[96m"
COLOR_BOLD = "\033[1m"

# --- Global variables for thread management ---
# Queue to hold ports to be scanned
port_queue = Queue()
# List to store open ports found
open_ports = []
# Lock for thread-safe access to open_ports list
print_lock = threading.Lock()

# --- Function to scan a single port ---
def scan_port(host, port, timeout):
    """
    Attempts to connect to a specific port on a given host.
    If successful, the port is considered open.
    """
    try:
        # Create a new socket object
        # AF_INET specifies the address family (IPv4)
        # SOCK_STREAM specifies the socket type (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for the connection attempt
        s.settimeout(timeout)

        # Attempt to connect to the host and port
        # connect_ex returns an error indicator instead of raising an exception
        result = s.connect_ex((host, port))

        # Check the result of the connection attempt
        if result == 0:
            # If result is 0, the connection was successful, meaning the port is open
            with print_lock:
                print(f"Port {port}: {COLOR_GREEN}{COLOR_BOLD}OPEN{COLOR_RESET}")
                open_ports.append(port)
        # else:
            # print(f"Port {port}: CLOSED or FILTERED") # Uncomment for verbose output

    except socket.gaierror:
        # Handle cases where the hostname cannot be resolved
        with print_lock:
            print(f"{COLOR_RED}Error: Hostname '{host}' could not be resolved. Exiting.{COLOR_RESET}")
        sys.exit()
    except socket.error as e:
        # Handle other socket-related errors
        with print_lock:
            print(f"{COLOR_YELLOW}Error connecting to port {port}: {e}{COLOR_RESET}")
    finally:
        # Ensure the socket is closed after each attempt
        s.close()

# --- Worker function for threads ---
def worker(host, timeout):
    """
    Worker function that continuously fetches ports from the queue
    and scans them until the queue is empty.
    """
    while True:
        # Get a port from the queue
        port = port_queue.get()
        # Scan the port
        scan_port(host, port, timeout)
        # Mark the task as done
        port_queue.task_done()

# --- Main function for the port scanner ---
def main():
    """
    Main function to get user input and orchestrate the port scanning.
    """
    # ASCII art of a crow
    crow_ascii = r"""
      _
     / \
    / _ \
   | (_) |
    \___/
    /   \
   |  o  |
   \_____/
    /   \
   |  _  |
   \ (_) /
    \___/
    """
    print(f"{COLOR_CYAN}{crow_ascii}{COLOR_RESET}")
    print(f"{COLOR_BOLD}{COLOR_BLUE}--- Noble Crow Port Scanner ---{COLOR_RESET}")
    print(f"{COLOR_YELLOW}Use responsibly and only on authorized networks.{COLOR_RESET}")

    # Get target host from user
    host = input(f"{COLOR_CYAN}Enter target host (e.g., 127.0.0.1, google.com) [{DEFAULT_HOST}]: {COLOR_RESET}")
    if not host:
        host = DEFAULT_HOST

    # Get port range from user
    port_range_input = input(f"{COLOR_CYAN}Enter port range (e.g., 1-1000) [{DEFAULT_START_PORT}-{DEFAULT_END_PORT}]: {COLOR_RESET}")
    if not port_range_input:
        start_port = DEFAULT_START_PORT
        end_port = DEFAULT_END_PORT
    else:
        try:
            start_port_str, end_port_str = port_range_input.split('-')
            start_port = int(start_port_str)
            end_port = int(end_port_str)
            if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535 and start_port <= end_port):
                print(f"{COLOR_RED}Invalid port range. Ports must be between 1 and 65535. Start port must be less than or equal to end port.{COLOR_RESET}")
                return
        except ValueError:
            print(f"{COLOR_RED}Invalid port range format. Please use 'start-end' (e.g., 1-1000).{COLOR_RESET}")
            return

    # Get timeout from user
    timeout_input = input(f"{COLOR_CYAN}Enter connection timeout in seconds [{DEFAULT_TIMEOUT}]: {COLOR_RESET}")
    try:
        timeout = float(timeout_input) if timeout_input else DEFAULT_TIMEOUT
        if not timeout > 0:
            print(f"{COLOR_RED}Timeout must be a positive number.{COLOR_RESET}")
            return
    except ValueError:
        print(f"{COLOR_RED}Invalid timeout value. Please enter a number.{COLOR_RESET}")
        return

    # Get number of threads from user (for faster scanning)
    num_threads_input = input(f"{COLOR_CYAN}Enter number of threads (e.g., 10, 50 for faster scan) [10]: {COLOR_RESET}")
    try:
        num_threads = int(num_threads_input) if num_threads_input else 10
        if not num_threads > 0:
            print(f"{COLOR_RED}Number of threads must be a positive integer.{COLOR_RESET}")
            return
    except ValueError:
        print(f"{COLOR_RED}Invalid number of threads. Please enter an integer.{COLOR_RESET}")
        return

    print(f"\n{COLOR_BLUE}Scanning {host} from port {start_port} to {end_port} with {num_threads} threads and {timeout}s timeout...{COLOR_RESET}")
    print(f"{COLOR_BLUE}{'-' * 40}{COLOR_RESET}")

    # Populate the port queue
    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    # Create and start worker threads
    for _ in range(num_threads):
        # daemon=True means threads will exit when the main program exits
        thread = threading.Thread(target=worker, args=(host, timeout), daemon=True)
        thread.start()

    # Wait for all tasks in the queue to be processed
    port_queue.join()

    print(f"{COLOR_BLUE}{'-' * 40}{COLOR_RESET}")
    if open_ports:
        print(f"{COLOR_GREEN}{COLOR_BOLD}Scan complete. Open ports on {host}: {sorted(open_ports)}{COLOR_RESET}")
        print(f"\n{COLOR_YELLOW}--- Next Steps for Open Ports ---{COLOR_RESET}")
        print(f"{COLOR_YELLOW}For each open port, you can try to identify the service running and its version. This often involves:{COLOR_RESET}")
        print(f"  {COLOR_CYAN}1.  {COLOR_BOLD}Banner Grabbing:{COLOR_RESET} Connect to the port and read the initial data sent by the service (e.g., `nc <host> <port>`).")
        print(f"  {COLOR_CYAN}2.  {COLOR_BOLD}Service Identification Tools:{COLOR_RESET} Use specialized tools like {COLOR_BOLD}Nmap{COLOR_RESET} (`nmap -sV <host> -p <port>`) to automatically detect service and version.")
        print(f"  {COLOR_CYAN}3.  {COLOR_BOLD}Web Browsing:{COLOR_RESET} If it's a common web port (80, 443, 8080), try navigating to `http://<host>:<port>` in your browser.")
        print(f"  {COLOR_CYAN}4.  {COLOR_BOLD}Common Port Knowledge:{COLOR_RESET} Research what services typically run on that specific port (e.g., 22 for SSH, 23 for Telnet, 25 for SMTP, 3389 for RDP).")
        print(f"  {COLOR_CYAN}5.  {COLOR_BOLD}Vulnerability Scanning:{COLOR_RESET} Once you know the service and version, you can look for known vulnerabilities associated with it.")
    else:
        print(f"{COLOR_YELLOW}Scan complete. No open ports found on {host} in the specified range.{COLOR_RESET}")

if __name__ == "__main__":
    main()
