import os
import torch
from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Load the tokenizer and model (example using GPT-2)
MODEL_NAME = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Set pad_token_id explicitly
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = tokenizer.eos_token_id
else:
    model.config.pad_token_id = tokenizer.pad_token_id

@app.route('/')
def index():
    """Render the index.html template."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Handle POST requests to generate responses using the GPT-2 model."""
    try:
        if request.is_json:
            data = request.json
            prompt = data.get('prompt', '')
            max_length = data.get('max_length', 50)
        else:
            return jsonify({'error': 'Request format not supported'}), 400

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        # Tokenize input text
        input_ids = tokenizer.encode(prompt, return_tensors='pt')

        # Generate text with attention_mask
        attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=input_ids.device)
        output = model.generate(input_ids, attention_mask=attention_mask, max_length=max_length)

        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

        return jsonify({'response': generated_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run Flask app with debug mode for development
    app.run(debug=True, host='0.0.0.0', port=9898)
