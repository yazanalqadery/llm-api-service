import asyncio
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


app = FastAPI()

class Settings(BaseSettings):
    api_key: str

class Item(BaseModel):
    name: str
    price: float

# class ExtractRequest(BaseModel):
#     text: str = Field(min_length=1, max_length=20)

MAX_CHARS = 20

class ExtractRequest(BaseModel):
    text: str = Field(min_length=1)

class ExtractResponse(BaseModel):
    chars: int

settings = Settings()

@app.post("/items")
def create_item(item: Item):
    return item

@app.post("/key-check")
def key_check():
    return {"has_key": bool(settings.api_key)}

# @app.post("/extract")
# def extract(req: ExtractRequest):
#     return {"chars": len(req.text)}

@app.post("/extract", response_model=ExtractResponse)
def extract(req: ExtractRequest):
    if len(req.text) > MAX_CHARS:
        raise HTTPException(
            status_code=413,
            detail=f"Text too long: {len(req.text)} characters, max is {MAX_CHARS}",
        )
    return {"chars": len(req.text)}

async def fake_tokens():
    for word in ["Hello", " from", " a", " streaming", " API"]:
        yield word
        await asyncio.sleep(0.5)

@app.get("/stream")
async def stream():
    return StreamingResponse(fake_tokens(), media_type="text/plain")

@app.get("/sse")
async def sse():
    async def events():
        for word in ["Hello", " from", " SSE"]:
            yield f"data: {word}\n\n"
            await asyncio.sleep(0.5)

    return StreamingResponse(events(), media_type="text/event-stream")

PAGE = """
<pre id="out"></pre>
<script>
  const es = new EventSource("/sse");
  es.onmessage = (e) => {
    document.getElementById("out").textContent += e.data;
  };
  es.onerror = () => es.close();
</script>
"""

@app.get("/test", response_class=HTMLResponse)
def test_page():
    return PAGE

@app.get("/health")
def health():
    return {"status": "ok"}
