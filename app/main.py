# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from pathlib import Path

from utils.config import settings
from chatbot import EventChatbot

app = FastAPI(title="EventEase Backend")

# CORS configuration
allowed_origins = ["*"] if settings.DEBUG else [
    settings.FRONTEND_ORIGIN,
    "https://*.ondigitalocean.app",  # Allow DO app platform domains
    "http://localhost:3000",  # Local development
    "http://localhost:5173"   # Vite dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Ensure data dirs exist
Path(settings.DATA_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.VECTOR_DIR).mkdir(parents=True, exist_ok=True)

# instantiate chatbot (loads vector db if exists)
bot = EventChatbot()

class ChatRequest(BaseModel):
    query: str
    conversation_id: str | None = None
    top_k: int | None = 4

@app.get("/health")
def health():
    return {"status": "ok", "service": "EventEase", "version": "0.1"}

@app.post("/ingest")
async def ingest(file: UploadFile = File(...), override: bool = False):
    """
    Upload a PDF or text file to ingest into vector store.
    """
    filename = file.filename
    target = os.path.join(settings.DATA_DIR, filename)

    # Save uploaded file
    with open(target, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        bot.ingest_document(target, override=override)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success", "filename": filename}

@app.post("/chat")
async def chat(req: ChatRequest):
    if not req.query or req.query.strip() == "":
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    answer = bot.answer_query(req.query, conversation_id=req.conversation_id, top_k=req.top_k or 4)
    return {"answer": answer}

