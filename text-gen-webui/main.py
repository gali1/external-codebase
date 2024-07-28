import os
import subprocess
import json
import threading
import time
from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from urllib.parse import quote
from werkzeug.serving import run_simple
from werkzeug.utils import secure_filename
import llama_cpp
# from gpt4all import GPT4All

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Retrieve OLLAMA_API_URL from environment variables, default to local endpoint
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://0.0.0.0:11434/api/generate")
# OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://gademo.net/api/generate")

# Create a ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=5)

# Initialize LLM models
local_models = {}

# Set up upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variables for download progress
download_progress = 0
is_downloading = False

def execute_shell_command(command):
    """Function to execute shell command."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.stderr}"

def generate_ssl_cert():
    """Generate SSL certificate if missing."""
    if not os.path.exists("cert.pem") or not os.path.exists("key.pem"):
        return execute_shell_command("sh gen-cert.sh")

@app.route("/")
def index():
    """Render the index.html template."""
    return render_template("index.html")

def generate_response_api(prompt, model, max_tokens=100):
    """Generate response using the external API."""
    try:
        response = requests.post(
            OLLAMA_API_URL, 
            json={"model": model, "prompt": prompt, "stream": False, "max_tokens": max_tokens},
            timeout=60
        )
        response.raise_for_status()
        return response.json().get("response"), None
    except requests.RequestException as e:
        return None, f"API Error: {str(e)}"

def generate_response_local(prompt, model, max_tokens=100):
    """Generate response using local LLM."""
    try:
        if model not in local_models:
            if model.endswith('.gguf'):
                local_models[model] = llama_cpp.Llama(model_path=os.path.join(app.config['UPLOAD_FOLDER'], model))
            else:
                local_models[model] = GPT4All(model_name=model)
        return local_models[model].generate(prompt, max_tokens=max_tokens), None
    except Exception as e:
        return None, f"Local LLM Error: {str(e)}"

def process_query(data):
    """Process the query and generate a response."""
    prompt = data.get("prompt", "").strip()
    model = data.get("model", "default_model").strip()
    use_api = data.get("use_api", True)
    max_tokens = data.get("max_tokens", 100)

    if not prompt:
        return jsonify({"error": "No prompt provided. Please enter a valid prompt."}), 400

    if not model:
        return jsonify({"error": "No model specified. Please select a model."}), 400

    if use_api:
        response, error = executor.submit(generate_response_api, prompt, model, max_tokens).result()
    else:
        if model not in local_models:
            if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], model)):
                global is_downloading, download_progress
                is_downloading = True
                download_progress = 0
                threading.Thread(target=download_model, args=(model,)).start()
                return jsonify({"downloading": True, "message": f"Downloading model: {model}"}), 202
        response, error = executor.submit(generate_response_local, prompt, model, max_tokens).result()

    if response:
        return jsonify({"response": response})
    else:
        error_message = error or "Unknown error occurred while generating response."
        return jsonify({"error": error_message}), 500

@app.route("/generate", methods=["POST"])
def generate():
    """Handle POST requests to generate responses."""
    try:
        data = request.get_json(force=True)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in request body"}), 400
    return process_query(data)

@app.route("/api/query", methods=["POST"])
def api_query():
    """Handle API queries on both HTTP and HTTPS."""
    try:
        data = request.get_json(force=True)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in request body"}), 400
    return process_query(data)

@app.route('/upload-model', methods=['POST'])
def upload_model():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(file_path)
            return jsonify({'success': True, 'message': f'File {filename} uploaded successfully'})
        except Exception as e:
            return jsonify({'success': False, 'error': f'Error saving file: {str(e)}'}), 500

@app.route('/download-progress')
def get_download_progress():
    global download_progress, is_downloading
    return jsonify({'progress': download_progress, 'is_downloading': is_downloading})

def download_model(model_name):
    global download_progress, is_downloading
    try:
        GPT4All.download_model(model_name, os.path.join(app.config['UPLOAD_FOLDER'], model_name))
        is_downloading = False
        download_progress = 100
    except Exception as e:
        print(f"Error downloading model: {str(e)}")
        is_downloading = False
        download_progress = 0

def monitor_services():
    """Monitor and restart services if needed."""
    # while True:
    #     try:
    #         response = requests.get(OLLAMA_API_URL, timeout=5)
    #         if response.status_code != 200:
    #             print(f"API server returned status code {response.status_code}. Restarting...")
    #             execute_shell_command("systemctl restart ollama")
    #     except requests.RequestException as e:
    #         print(f"Error connecting to API server: {str(e)}. Restarting...")
    #         execute_shell_command("systemctl restart ollama")

    #     # Check local LLM processes
    #     for model_name, model in local_models.items():
    #         if not model.is_alive():
    #             print(f"Local model {model_name} is not responding. Restarting...")
    #             del local_models[model_name]
    #             # Reinitialize the model in the next query

    #     time.sleep(60)  # Check every minute

if __name__ == "__main__":
    cert_result = generate_ssl_cert()
    print(f"SSL Certificate generation result: {cert_result}")

    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor_services, daemon=True)
    monitor_thread.start()

    try:
        # Run the app on both HTTP and HTTPS using run_simple
        threading.Thread(target=run_simple, args=('0.0.0.0', 8877, app), kwargs={'use_reloader': False, 'use_debugger': True}, daemon=True).start()
        run_simple('0.0.0.0', 9899, app, use_reloader=False, use_debugger=True, ssl_context=('cert.pem', 'key.pem'))
    except Exception as e:
        print(f"Error starting servers: {e}")
