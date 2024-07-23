import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Load model and tokenizer
MODEL_NAME = os.getenv("MODEL_NAME", "gpt2")  # Default to GPT-2, change as needed
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Create a ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=5)

# Set batch size
BATCH_SIZE = 128

@app.route("/")
def index():
    """Render the index.html template."""
    return render_template("index.html")

def generate_response(prompt, max_length=100):
    """Generate response using the model directly."""
    try:
        # Tokenize input
        input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
        
        # Generate text in batches
        output = []
        for i in range(0, max_length, BATCH_SIZE):
            batch_length = min(BATCH_SIZE, max_length - i)
            batch_output = model.generate(
                input_ids,
                max_length=input_ids.shape[1] + batch_length,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.7
            )
            
            # Decode and add to output
            batch_text = tokenizer.decode(batch_output[0], skip_special_tokens=True)
            output.append(batch_text[len(prompt):])
            
            # Update input_ids for next iteration
            input_ids = batch_output

        return "".join(output)
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return None

@app.route("/generate", methods=["POST"])
def generate():
    """Handle POST requests to generate responses."""
    data = request.json
    prompt = data["prompt"]
    max_length = data.get("max_length", 100)

    # Use ThreadPoolExecutor to run the generation asynchronously
    future = executor.submit(generate_response, prompt, max_length)
    response = future.result()

    if response:
        return jsonify({"response": response})
    else:
        return jsonify({"error": "Error generating response"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9898, threaded=True)