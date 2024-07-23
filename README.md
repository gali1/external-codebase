# AI Query Interface for GitHub Codespaces

This project sets up a JupyterLab environment with a text-based interface for generating responses using the Ollama API, designed to run smoothly in GitHub Codespaces. It features a simple web UI for user queries, a backend to interact with the Ollama API, and optimizations for speed and performance.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup Instructions](#setup-instructions)
3. [File Structure](#file-structure)
4. [Code Breakdown](#code-breakdown)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

- GitHub account
- Access to GitHub Codespaces
- Basic knowledge of Python, Flask, and HTML

## Setup Instructions

1. Create a new repository on GitHub.
2. Open the repository in GitHub Codespaces.
3. In the Codespaces environment, create the following files with the contents provided in the [File Structure](#file-structure) section:
   - `main.py`
   - `templates/index.html`
   - `requirements.txt`
   - `.env`
4. Open a terminal in Codespaces and run the following commands:

   ```bash
   pip install -r requirements.txt
   ```

5. Install Ollama (if not already available in Codespaces):

   ```bash
   curl https://ollama.ai/install.sh | sh
   ```

6. Start the Ollama server in the background:

   ```bash
   ollama run llama2 &
   ```

7. Start the Flask application:

   ```bash
   python main.py
   ```

8. Open the web interface using the provided URL in the Codespaces environment.

## File Structure

### main.py

```python
import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Retrieve OLLAMA_API_URL from environment variables, default to local endpoint
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/generate')

# Use a requests Session for connection pooling
session = requests.Session()

@app.route('/')
def index():
    """Render the index.html template."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Handle POST requests to generate responses using the external API."""
    try:
        data = request.json
        prompt = data['prompt']
        model = data['model']

        # Send POST request to external API using session
        response = session.post(OLLAMA_API_URL, json={
            'model': model,
            'prompt': prompt,
            'stream': False
        })

        # Check response status and return JSON response
        response.raise_for_status()
        return jsonify({'response': response.json()['response']})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request to external API failed: {str(e)}'}), 500

    except KeyError as e:
        return jsonify({'error': f'Missing required parameter: {str(e)}'}), 400

if __name__ == '__main__':
    # Run the application in production mode
    app.run(debug=False, host='0.0.0.0', port=9898)
```

### templates/index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Query Interface</title>
    <style>
        /* Reset default margin and padding */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        
        .container {
            max-width: 500px;
            width: 100%;
            background-color: #ffffff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        
        h1 {
            font-size: 24px;
            margin-bottom: 20px;
            text-align: center;
            color: #333333;
        }
        
        select, textarea, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #dddddd;
            border-radius: 4px;
            background-color: #f5f5f5;
            font-size: 14px;
            color: #555555;
        }
        
        button {
            background-color: #007bff;
            color: #ffffff;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        button:hover {
            background-color: #0056b3;
        }
        
        #response {
            margin-top: 15px;
            padding: 15px;
            background-color: #f5f5f5;
            border: 1px solid #dddddd;
            border-radius: 4px;
            white-space: pre-wrap;
            font-size: 14px;
            color: #333333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Query Interface</h1>
        <select id="model">
            <option value="llama2">Llama 2</option>
            <option value="mistral">Mistral</option>
            <option value="vicuna">Vicuna</option>
        </select>
        <textarea id="prompt" rows="4" placeholder="Enter your query here..."></textarea>
        <button onclick="generateResponse()">Generate Response</button>
        <div id="response"></div>
    </div>

    <script>
        async function generateResponse() {
            const prompt = document.getElementById('prompt').value;
            const model = document.getElementById('model').value;
            const responseDiv = document.getElementById('response');

            responseDiv.textContent = 'Generating response...';

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ prompt, model }),
                });

                if (response.ok) {
                    const data = await response.json();
                    responseDiv.textContent = data.response;
                } else {
                    responseDiv.textContent = 'Error generating response';
                }
            } catch (error) {
                responseDiv.textContent = 'Error: ' + error.message;
            }
        }
    </script>
</body>
</html>

```

### requirements.txt

```
Flask==2.0.2
Werkzeug==2.0.3
requests==2.26.0
python-dotenv==0.19.1
aiohttp
python-dotenv hypercorn
```

### .env

```
OLLAMA_API_URL=http://localhost:11434/api/generate
```

## Code Breakdown

### main.py

This file contains the Flask application that serves as the backend for our AI Query Interface.

- We import necessary libraries and load environment variables from the `.env` file.
- The Flask app is initialized and configured to use the Ollama API URL from the environment variables.
- Two routes are defined:
  1. The root route ('/') serves the HTML template.
  2. The '/generate' route handles POST requests to generate responses using the Ollama API.
- The generate function extracts the prompt and model from the request, sends a request to the Ollama API, and returns the response.

### index.html

This file contains the HTML and JavaScript for the frontend of our AI Query Interface.

- The HTML structure includes a dropdown for model selection, a textarea for the user's prompt, and a button to generate a response.
- CSS styles are included in the `<style>` tag to create a dark-themed interface.
- JavaScript is used to handle the form submission and API interaction:
  - The `generateResponse()` function is called when the button is clicked.
  - It sends a POST request to the '/generate' endpoint with the user's prompt and selected model.
  - The response is then displayed in the `#response` div.

## Running the Application

1. Ensure all files are created and Ollama is running in the background.
2. In the terminal, run:

   ```bash
   python main.py
   ```

3. Open the provided URL to access the web interface.
4. Select a model from the dropdown, enter your query in the textarea, and click "Generate Response".

## Troubleshooting

- If you encounter issues with Ollama, ensure it's properly installed and running in the background.
- Check the Codespaces logs for any error messages related to Flask or the Ollama API.
- Verify that the `OLLAMA_API_URL` in the `.env` file is correct for your Codespaces environment.

Remember to respect copyright laws and terms of service when using and deploying language models. Always ensure you have the necessary rights and permissions for the models and content you're using.
