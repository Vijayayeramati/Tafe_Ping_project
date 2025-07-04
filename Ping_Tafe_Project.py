import ping3
import socket
import re
from datetime import datetime

# Configure ping3
ping3.EXCEPTIONS = True
ping3.TIMEOUT = 2  # seconds

log_file = "ping_log.txt"

# Validate hostnames using basic regex
def is_valid_hostname(hostname):
    pattern = re.compile(r"^(?!-)[A-Za-z0-9.-]{1,253}(?<!-)$")
    #return pattern.match(hostname) != None
    match = pattern.match(hostname)
    if match:
        return True
    else:
        return False

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def display_host_list(hosts):
    print("\nHost List:")
    for i, host in enumerate(hosts):
        print(f"{i}: {host}")
    print()

def ping_host(host):
    try:
        ip = socket.gethostbyname(host)
        response = ping3.ping(ip)
        if response is None:
            print(f" Timeout: No reply from {host} ({ip})")
            log(f"TIMEOUT - {host} ({ip})")
            return False
        else:
            ms_time = round(response * 1000, 2)
            print(f" Reply from {host} ({ip}) in {ms_time} ms")
            log(f"SUCCESS - {host} ({ip}) in {ms_time} ms")
            return True
    except (socket.gaierror, ping3.errors.PingError) as e:
        print(f" Error: {host} could not be resolved or pinged.")
        log(f"ERROR - {host} - {e}")
        return False

def main():
    hosts = []
    print("Hostname Ping Tool (TAFE - CyberSec Script)")

    while True:
        entry = input("Enter a hostname (press Enter to finish): ").strip()
        if not entry:
            break
        if not is_valid_hostname(entry):
            print("Invalid hostname format. Try again.")
            continue
        hosts.append(entry)

    if not hosts:
        print(" No valid hostnames entered. Exiting.")
        return

    success_count = 0
    failure_count = 0

    while True:
        display_host_list(hosts)
        index_input = input("Enter an index to ping a host (or press Enter to exit): ").strip()

        if not index_input:
            print("Exiting. Goodbye.")
            break

        try:
            index = int(index_input)
            if 0 <= index < len(hosts):
                result = ping_host(hosts[index])
                if result:
                    success_count += 1
                else:
                    failure_count += 1
            else:
                print("Index out of range.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    print(f"\n Ping Summary: {success_count} succeeded, {failure_count} failed")
    print(f" Details logged to {log_file}")

if __name__ == "__main__":
    main()
