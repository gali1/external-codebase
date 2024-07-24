import subprocess
import socket
import time

def is_port_in_use(port):
    # Check if the specified port is in use
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("localhost", port))
        except socket.error:
            return True
        return False

def run_main_script():
    # Port to monitor
    port_to_monitor = 11434
    
    while True:
        print(f"Checking if port {port_to_monitor} is active...")
        
        if is_port_in_use(port_to_monitor):
            print(f"Port {port_to_monitor} is active. Starting main.py...")
            try:
                # Use subprocess to start main.py as a separate process
                process = subprocess.Popen(["python3", "/workspaces/external-codebase/main.py"])
                # Wait for the process to finish (which ideally should not happen)
                process.wait()
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f"Port {port_to_monitor} is not active. Starting 'ollama serve'...")
            try:
                # Execute the 'ollama serve' command
                subprocess.run(["ollama", "serve"])
            except Exception as e:
                print(f"Error: {e}")
        
        print(f"Restarting in 3 seconds...")
        time.sleep(3)

if __name__ == "__main__":
    run_main_script()
