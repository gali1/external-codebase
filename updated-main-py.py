import os
import subprocess
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from werkzeug.serving import WSGIServer

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Retrieve OLLAMA_API_URL from environment variables, default to local endpoint
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "https://automatic-waffle-jj4w7w644px25447-11434.app.github.dev/api/generate")
# OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://automatic-waffle-jj4w7w644px25447-11434.app.github.dev:443/api/generate")

# Create a ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=5)

def execute_shell_command():
    """Function to execute shell command."""
    command = "fuser -k 80/tcp; fuser -k 443/tcp; source ~/.bashrc"
    subprocess.run(command, shell=True)

@app.route("/")
def index():
    """Render the index.html template."""
    return render_template("index.html")

def generate_response(prompt, model):
    """Generate response using the external API."""
    try:
        response = requests.post(
            OLLAMA_API_URL, 
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=60
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.RequestException:
        execute_shell_command()
        return None

@app.route("/generate", methods=["POST"])
def generate():
    """Handle POST requests to generate responses using the external API."""
    data = request.json
    prompt = data["prompt"]
    model = data["model"]

    # Use ThreadPoolExecutor to run the API call asynchronously
    future = executor.submit(generate_response, prompt, model)
    response = future.result()

    if response:
        return jsonify({"response": response})
    else:
        return jsonify({"error": "Error generating response"}), 500

@app.route("/api/query", methods=["POST"])
def api_query():
    """Handle API queries on both HTTP and HTTPS."""
    data = request.json
    prompt = data.get("prompt")
    model = data.get("model", "default-model")  # Use a default model if not specified

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    response = generate_response(prompt, model)
    if response:
        return jsonify({"response": response})
    else:
        return jsonify({"error": "Error generating response"}), 500

if __name__ == "__main__":
    # Run the app on both HTTP and HTTPS
    http_server = WSGIServer(('0.0.0.0', 80), app)
    https_server = WSGIServer(('0.0.0.0', 443), app, ssl_context=('path/to/cert.pem', 'path/to/key.pem'))

    # Run servers in separate threads
    from threading import Thread
    Thread(target=http_server.serve_forever).start()
    Thread(target=https_server.serve_forever).start()
