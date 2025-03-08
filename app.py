import json
import time
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

app = FastAPI()


# -----------------------------
# Request & Response Models
# -----------------------------
class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    stream: Optional[bool] = False
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = 100


# -----------------------------
# Streaming Generator
# -----------------------------
def generate_chat_stream():
    sample_text = "This is a streamed response."
    for word in sample_text.split():
        time.sleep(1)
        yield f'data: {{"choices": [{{"delta": {{"content": "{word} "}}, "index": 0}}]}}\n\n'
    yield "data: [DONE]\n\n"


# -----------------------------
# Chat Completions Endpoint
# -----------------------------
@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    if request.stream:
        return StreamingResponse(generate_chat_stream(), media_type="text/event-stream")
    else:
        return JSONResponse(
            content={
                "id": "chatcmpl-12345",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": request.model,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": "This is a static response.",
                        },
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                },
            }
        )


# -----------------------------
# Image Generation Endpoint
# -----------------------------
@app.post("/v1/images/generations")
async def image_generation():
    return JSONResponse(
        content={
            "created": int(time.time()),
            "data": [{"url": "https://dummyimage.com/512x512/000/fff.png"}],
        }
    )


# -----------------------------
# Other API Endpoints (Placeholder Implementations)
# -----------------------------
@app.post("/v1/completions")
async def completions():
    return JSONResponse(
        content={"choices": [{"text": "This is a static completion response."}]}
    )


@app.post("/v1/embeddings")
async def embeddings():
    return JSONResponse(content={"data": [{"embedding": [0.1, 0.2, 0.3]}]})


@app.post("/v1/audio/transcriptions")
async def transcriptions():
    return JSONResponse(content={"text": "This is a static transcription."})


@app.post("/v1/audio/speech")
async def audio_speech():
    return JSONResponse(content={"audio_url": "https://dummy-audio.com/sample.mp3"})


# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
