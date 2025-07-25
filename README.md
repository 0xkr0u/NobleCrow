Noble Crow Port Scanner
The Noble Crow Port Scanner is a lightweight, multi-threaded network utility written in Python. It's designed to help you identify open TCP ports on a target host within a specified range. With its distinctive ASCII art crow and colored output, it provides a clear and engaging way to perform basic network reconnaissance.

Disclaimer: This tool is for educational purposes and for use on networks or hosts for which you have explicit permission to scan. Unauthorized port scanning can be illegal and unethical. Please use it responsibly.

Features
Multi-threaded Scanning: Utilizes Python's threading module to scan multiple ports concurrently, significantly speeding up the process.

Configurable Scan Range: You can define the starting and ending ports for the scan, including the full range from 1 to 65535.

Customizable Timeout: Set a connection timeout to control how long the scanner waits for a response from each port.

Colored Output: Uses ANSI escape codes to provide clear, color-coded output for open ports and status messages.

Noble Crow ASCII Art: A unique ASCII art crow greets you upon startup.

Prerequisites
To run this program, you need:

Python 3.x (preferably the latest stable version).

You can check if Python 3 is installed by opening your terminal or command prompt and typing:

python3 --version

If you don't have Python 3, you can download it from python.org. Remember to check "Add Python to PATH" during installation on Windows.

Installation
There's no complex installation process. Simply:

Save the code: Copy the entire Python code for the "Noble Crow Port Scanner" into a plain text file.

Name the file: Save the file with a .py extension (e.g., noble_crow_scanner.py).

Usage
Open your terminal or command prompt.

Navigate to the directory where you saved noble_crow_scanner.py (or whatever you named it). For example:

cd /path/to/your/script/

Run the program using Python 3:

python3 noble_crow_scanner.py

Follow the prompts: The program will guide you through the necessary inputs:

Enter target host: Provide an IP address (e.g., 192.168.1.1) or a hostname (e.g., example.com). Default is 127.0.0.1 (localhost).

Enter port range: Specify a range like 1-1000. Default is 1-65535.

Enter connection timeout in seconds: A float value like 0.5 or 1. Default is 1.

Enter number of threads: An integer like 10 or 50 for faster scanning. Default is 10.

Example Scan:
python3 noble_crow_scanner.py

  _
 / \
/ _ \

| () |
___/
/

|  o  |
___/
/

|  _  |
\ () /
___/
--- Noble Crow Port Scanner ---
Use responsibly and only on authorized networks.
Enter target host (e.g., 127.0.0.1, https://www.google.com/search?q=google.com) [127.0.0.1]:
Enter port range (e.g., 1-1000) [1-65535]: 80-90
Enter connection timeout in seconds [1]: 0.5
Enter number of threads (e.g., 10, 50 for faster scan) [10]: 20

Scanning 127.0.0.1 from port 80 to 90 with 20 threads and 0.5s timeout...
Port 80: OPEN
Scan complete. Open ports on 127.0.0.1: [80]

--- Next Steps for Open Ports ---
For each open port, you can try to identify the service running and its version. This often involves:

Banner Grabbing: Connect to the port and read the initial data sent by the service (e.g., nc <host> <port>).

Service Identification Tools: Use specialized tools like Nmap (nmap -sV <host> -p <port>) to automatically detect service and version.

Web Browsing: If it's a common web port (80, 443, 8080), try navigating to http://<host>:<port> in your browser.

Common Port Knowledge: Research what services typically run on that specific port (e.g., 22 for SSH, 23 for Telnet, 25 for SMTP, 3389 for RDP).

Vulnerability Scanning: Once you know the service and version, you can look for known vulnerabilities associated with it.


## Contributing

Feel free to fork this repository, suggest improvements, or add new features!

## License

This project is open-source.
