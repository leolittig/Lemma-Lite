import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

from mlx_vlm import load
from mlx_vlm.generate import stream_generate
from mlx_vlm.prompt_utils import apply_chat_template

model, processor = load("mlx-community/gemma-4-12B-it-8bit")
history = []
app = FastAPI()

class Msg(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
def index():
    return open("index.html").read()

@app.post("/chat")
async def chat(msg: Msg):
    history.append({"role": "user", "content": [{"type": "text", "text": msg.text}]})
    formatted = apply_chat_template(processor, model.config, history, num_images=0)

    async def generate():
        reply = ""
        for chunk in stream_generate(model, processor, formatted, image=None, max_tokens=2048, temperature=1.0):
            reply += chunk.text
            yield chunk.text
        history.append({"role": "assistant", "content": [{"type": "text", "text": reply.replace("<end_of_utterance>", "").strip()}]})

    return StreamingResponse(generate(), media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
