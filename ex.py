import subprocess

def expose_port(port):
    try:
        # Add firewall rule to allow incoming traffic on specified port
        subprocess.run(['', 'iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', str(port), '-j', 'ACCEPT'])
        subprocess.run(['sudo', 'iptables-save'])
        print(f"Port {port} has been exposed.")
    except Exception as e:
        print(f"Failed to expose port {port}: {e}")

if __name__ == "__main__":
    port = input("Enter the port number to expose: ")
    expose_port(port)
