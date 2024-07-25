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


def start_main_script():
    try:
        subprocess.run(["python3", "/workspaces/external-codebase/main.py"])
    except Exception as e:
        print(f"Error starting main.py: {e}")


def run_main_script():
    # Port to monitor
    port_to_monitor = 9898

    while True:
        print(f"Checking if port {port_to_monitor} is active...")

        if is_port_in_use(port_to_monitor):
            print(f"Port {port_to_monitor} is active. Starting main.py...")
            start_main_script()
        else:
            print(f"Port {port_to_monitor} is not active. Starting 'ollama serve'...")
            try:
                # Execute the 'ollama serve' command
                subprocess.run(["ollama", "serve"])
            except Exception as e:
                print(f"Error starting 'ollama serve': {e}")

        print(f"Restarting script in 3 seconds...")
        time.sleep(3)


if __name__ == "__main__":
    run_main_script()
