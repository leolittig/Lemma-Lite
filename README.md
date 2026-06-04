# Lemma

A lightweight LLM chat interface optimized for Apple Silicon using MLX. A web version of the terminal UI that supports Markdown formatting outputs for a cleaner view.

## How it Works

1. **Frontend ([index.html](index.html))**: A simple chat UI. It sends user queries to `/chat` and uses a `ReadableStream` reader to decode and render the Markdown response chunk-by-chunk as it arrives.
2. **Backend ([app.py](app.py))**: A FastAPI server that loads the model using `mlx-vlm`. It appends new messages to a global conversation history, applies the model's chat template, and yields generated tokens over a `StreamingResponse`.

## Quick Start

### 1. Set Up Virtual Environment
Create and activate the virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
Install the required dependencies listed in [requirements.txt](requirements.txt):
```bash
pip install -r requirements.txt
```

### 3. Run the Server
Start the chat application:
```bash
python app.py
```
Then visit `http://127.0.0.1:8000` in your browser.

## Changing the Model
To swap the model, change the Hugging Face repo path in [app.py](app.py#L13):
```python
# Replace with any MLX-compatible Hugging Face model
model, processor = load("mlx-community/gemma-4-12B-it-8bit")
```
