import subprocess
import time

def run_main_script():
    while True:
        print("Starting main.py...")
        try:
            # Use subprocess to start main.py as a separate process
            process = subprocess.Popen(["python3", "main.py"])
            process = subprocess.Popen(["ollama", "serve"])
            # Wait for the process to finish (which ideally should not happen)
            process.wait()
        except Exception as e:
            print(f"Error: {e}")
        
        print("main.py has exited. Restarting in 3 seconds...")
        time.sleep(3)

if __name__ == "__main__":
    run_main_script()
