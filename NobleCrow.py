# Arthur: 0xkr0u
import argparse
import socket
from concurrent.futures import ThreadPoolExecutor
try:
    # ANSI color codes
    GREEN = "\033[92m"
    RED   = "\033[91m"
    YELLOW= "\033[93m"
    CYAN  = "\033[96m"
    PURPLE = "\033[35m"
    RESET = "\033[0m"
    ascii_art = (
        " ___..-\"\"\"-.  `)^|   .-\"\"\"-..___\n"
        "`-...___ '=.'-.'  \\-'.=' ___...-'\n"
        "        `\\  ' Crow '  /`\n"
        "          '--;|||||;--'\n"
        "             /\\|||/\\\n"
        "      kr0u  ( /;-;\\ )\n"
        "             '-...-'\n"
    )

# =================================== Connection ===================================
    
    def scan(port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((ip_address, port)) == 0:
                    print(f"{GREEN}[+] {port} OPEN{RESET}")

        except Exception as e:
            print(f"{YELLOW}[!] Error on port {port}: {e}{RESET}")

# =================================== commands ===================================

    parser = argparse.ArgumentParser(prog="NetScan", description="Lightweight custom enumerator")
    parser.add_argument("-d","--domain", help="Resolve a domain to an IP address")
    parser.add_argument("-i","--ip", help="Target IP address to scan")
    parser.add_argument("-t","--start", type=int, default=1, help="Minimum port number")
    parser.add_argument("-e","--end", type=int, default=65535, help="Maximum port number")
    parser.add_argument("-T","--threads", type=int, default=100, help="Ports per batch")
    args = parser.parse_args()

    # Custom prints before the script runns 
    print(f"{PURPLE}{ascii_art}{RESET}")
    print(f"{GREEN} FULL usage: script.py -d example.com -t 0 -e 65535  {RESET}")
    print(f"{RED}Default settings:\n-e: 65535\n-t: 1")

# Resolve domain or set IP
    if args.domain:
        try:
            ip_address = socket.gethostbyname(args.domain.strip())
            print(f"{CYAN}[*] Scanning resolved domain: {ip_address}{RESET}")
        except OSError as e:
            print(f"{YELLOW}[!] Could not resolve domain: {e}{RESET}")
            exit(1)
    elif args.ip:
        ip_address = args.ip
        print(f"{CYAN}[*] Scanning IP: {ip_address}{RESET}")
    else:
        ip_address = "127.0.0.1"
        print(f"{CYAN}[*] No target specified, defaulting to 127.0.0.1{RESET}")

# Threaded scanning
    for start in range(args.start, args.end, args.threads):
        end = min(start + args.threads, args.end)
        with ThreadPoolExecutor() as executor:
            executor.map(scan, range(start, end))




except KeyboardInterrupt:
    print(f"\n{YELLOW}[!] Keyboard Interrupt detected{RESET}")
    print(f"{YELLOW}[!]Aborting{RESET}")
    print(f"{YELLOW}[*]Thank you for using the script{RESET}")
