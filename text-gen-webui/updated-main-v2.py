import os
import subprocess
from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from werkzeug.serving import run_simple
from werkzeug.utils import secure_filename
import llama_cpp
from gpt4all import GPT4All
import threading
import time
import logging
import signal
import sys
from flask_cors import CORS


# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Retrieve OLLAMA_API_URL from environment variables, default to local endpoint
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")

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

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def execute_shell_command(command):
    """Function to execute shell command."""
    subprocess.run(command, shell=True)

def generate_ssl_cert():
    """Generate SSL certificate if missing."""
    if not os.path.exists("cert.pem") or not os.path.exists("key.pem"):
        execute_shell_command("bash gen-cert.sh")

def parse_model_name(model_name):
    """Parse model name and tag."""
    if ':' in model_name:
        model, tag = model_name.split(':', 1)
    else:
        model = model_name
        tag = 'latest'
    return model, tag

def generate_response_api(prompt, model, params):
    """Generate response using the external API."""
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": params.get("stream", False),
                **params
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error with API request: {e}")
        return None

def generate_response_local(prompt, model, params):
    """Generate response using local LLM."""
    try:
        if model not in local_models:
            if model.endswith('.gguf'):
                local_models[model] = llama_cpp.Llama(model_path=os.path.join(app.config['UPLOAD_FOLDER'], model))
            else:
                local_models[model] = GPT4All(model_name=model)
        return local_models[model].generate(prompt, max_tokens=100)
    except Exception as e:
        logger.error(f"Error generating local response: {e}")
        return None

@app.route("/")
def index():
    """Render the index.html template."""
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    """Handle POST requests to generate responses."""
    global is_downloading, download_progress
    try:
        data = request.json
        prompt = data.get("prompt")
        model = data.get("model")
        use_api = data.get("use_api", True)
        params = data.get("params", {})

        if not prompt or not model:
            return jsonify({"error": "Missing 'prompt' or 'model' in request"}), 400

        model, tag = parse_model_name(model)
        if use_api:
            future = executor.submit(generate_response_api, prompt, model, params)
        else:
            if model not in local_models:
                if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], model)):
                    is_downloading = True
                    download_progress = 0
                    threading.Thread(target=download_model, args=(model,)).start()
                    return jsonify({"downloading": True})

            future = executor.submit(generate_response_local, prompt, model, params)

        response = future.result(timeout=60)

        if response:
            return jsonify({"response": response})
        else:
            return jsonify({"error": "Error generating response"}), 500
    except KeyError as e:
        return jsonify({"error": f"KeyError: {e}"}), 400
    except Exception as e:
        logger.error(f"Exception in /generate endpoint: {e}")
        return jsonify({"error": f"Exception: {e}"}), 500

@app.route('/upload-model', methods=['POST'])
def upload_model():
    """Upload a new model to the server."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'success': True})

@app.route('/download-progress')
def get_download_progress():
    """Get the progress of model download."""
    global download_progress, is_downloading
    return jsonify({'progress': download_progress, 'is_downloading': is_downloading})

def download_model(model_name):
    """Download model and save it to the server."""
    global download_progress, is_downloading
    try:
        # Implement download logic here, I'm assuming GPT4All.download_model is a placeholder
        # Replace this with actual downloading logic based on your requirements
        GPT4All.download_model(model_name, os.path.join(app.config['UPLOAD_FOLDER'], model_name))
        is_downloading = False
        download_progress = 100
    except Exception as e:
        logger.error(f"Error downloading model: {e}")
        is_downloading = False
        download_progress = 0

def monitor_services():
    """Monitor and restart services if needed."""
    while True:
        try:
            # Check API server
            requests.get(OLLAMA_API_URL, timeout=10)
        except requests.RequestException as e:
            logger.error(f"Error checking API server: {e}")
            # Implement restart logic here if necessary

        # Check local LLM processes
        # Implement logic to monitor and restart local LLM processes if needed

        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    generate_ssl_cert()

    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor_services, daemon=True)
    monitor_thread.start()

    # Set up signal handling in the main thread
    def signal_handler(sig, frame):
        logger.info(f"Received signal {sig}. Exiting...")
        # Clean up tasks can be added here if needed
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        # Run the app on both HTTP and HTTPS using run_simple
        http_thread = threading.Thread(target=run_simple, args=('0.0.0.0', 8877, app), kwargs={'use_reloader': True, 'use_debugger': True, 'threaded': True})
        http_thread.start()

        run_simple('0.0.0.0', 9899, app, use_reloader=True, use_debugger=True, ssl_context=('cert.pem', 'key.pem'), threaded=True)
    except Exception as e:
        logger.error(f"Error starting servers: {e}")
