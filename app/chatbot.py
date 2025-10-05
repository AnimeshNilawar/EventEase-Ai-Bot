# app/chatbot.py
import os
from typing import List
from utils.vector_store import VectorStore
from utils.loader import load_document_chunks
from utils.config import settings
import json
import requests
import logging

# OpenAI fallback removed to enforce Gradient-only usage
openai = None

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# Read gradient settings via config/settings or env
USE_GRADIENT_ENV = os.getenv("USE_GRADIENT", "true")
USE_GRADIENT_SETTINGS = getattr(settings, "USE_GRADIENT", True)
USE_GRADIENT = (USE_GRADIENT_ENV.lower() in ("1", "true", "yes") if isinstance(USE_GRADIENT_ENV, str) else USE_GRADIENT_ENV) or USE_GRADIENT_SETTINGS
GRADIENT_API_KEY = os.getenv("GRADIENT_API_KEY") or getattr(settings, "GRADIENT_API_KEY", None)
GRADIENT_API_BASE = os.getenv("GRADIENT_API_BASE", getattr(settings, "GRADIENT_API_BASE", "https://apis.gradient.network"))
GRADIENT_MODEL = os.getenv("GRADIENT_MODEL", getattr(settings, "GRADIENT_MODEL", "gpt-4o-mini"))

# Debug logging
LOGGER.info(f"USE_GRADIENT: {USE_GRADIENT}")
LOGGER.info(f"GRADIENT_API_KEY: {'***' + GRADIENT_API_KEY[-4:] if GRADIENT_API_KEY else 'NOT SET'}")
LOGGER.info(f"GRADIENT_API_BASE: {GRADIENT_API_BASE}")
LOGGER.info(f"GRADIENT_MODEL: {GRADIENT_MODEL}")

# OpenAI settings removed - using Gradient AI only

class EventChatbot:
    def __init__(self):
        """
        Initialize vector store (loads persisted index if present).
        """
        self.vs = VectorStore(vector_dir=settings.VECTOR_DIR)
        self.conversations = {}

    def ingest_document(self, filepath: str, override: bool = False):
        chunks = load_document_chunks(filepath)
        self.vs.add_documents(chunks, override=override)
        return {"added": len(chunks)}

    def retrieve(self, query: str, top_k: int = 4):
        return self.vs.similarity_search(query, k=top_k)

    def _build_prompt(self, query: str, contexts: List[dict], conv_history: List[dict] | None = None):
        system = (
            "You are EventEase — an assistant answering user questions about an event. "
            "Answer concisely and cite any relevant context chunk id when helpful."
        )
        ctx_texts = "\n\n".join([f"CHUNK_ID:{c['id']}\n{c['text']}" for c in contexts])
        prompt_parts = [system, f"Context:\n{ctx_texts}", "Conversation:"]
        if conv_history:
            for m in conv_history:
                prompt_parts.append(f"{m['role'].upper()}: {m['text']}")
        prompt_parts.append(f"USER: {query}")
        prompt_parts.append("ASSISTANT:")
        return "\n\n".join(prompt_parts)

    def _call_gradient_chat(self, prompt: str, max_tokens: int = 300, temperature: float = 0.7):
        """
        Calls DigitalOcean Gradient AI Serverless Inference API.
        Documentation: https://docs.digitalocean.com/products/ai-ml/gradient/how-to/serverless-inference/
        """
        if not GRADIENT_API_KEY:
            raise RuntimeError("GRADIENT_API_KEY not set.")

        # Use the official DigitalOcean Gradient AI endpoint
        url = f"{GRADIENT_API_BASE}/v1/chat/completions"
        
        LOGGER.info(f"Calling DigitalOcean Gradient AI: {url}")
        LOGGER.info(f"Using model: {GRADIENT_MODEL}")
        
        headers = {
            "Authorization": f"Bearer {GRADIENT_API_KEY}",
            "Content-Type": "application/json",
        }
        
        # Format according to DigitalOcean Gradient AI documentation
        payload = {
            "model": GRADIENT_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            LOGGER.info(f"Response status: {resp.status_code}")
            
            if resp.status_code == 200:
                data = resp.json()
                LOGGER.info(f"Response received: {data}")
                # Handle DigitalOcean Gradient AI response format
                if "choices" in data and len(data["choices"]) > 0:
                    message = data["choices"][0].get("message", {})
                    content = message.get("content", "")
                    return content.strip()
                else:
                    LOGGER.warning(f"Unexpected response format: {data}")
                    return "Response received but format not recognized."
            else:
                LOGGER.error(f"API returned status {resp.status_code}: {resp.text[:200]}")
                raise RuntimeError(f"DigitalOcean Gradient AI API error: {resp.status_code} - {resp.text[:200]}")
                
        except requests.exceptions.RequestException as e:
            LOGGER.error(f"Request failed: {e}")
            raise RuntimeError(f"Failed to connect to DigitalOcean Gradient AI: {e}")

    # OpenAI function removed - using Gradient AI only

    def answer_query(self, query: str, conversation_id: str | None = None, top_k: int = 4):
        conv_history = None
        if conversation_id:
            conv_history = self.conversations.get(conversation_id, [])

        contexts = self.retrieve(query, top_k=top_k)
        prompt = self._build_prompt(query, contexts, conv_history)

        # Use Gradient AI only; hard error if it fails
        try:
            answer = self._call_gradient_chat(prompt)
            LOGGER.info("Successfully got response from Gradient AI")
        except Exception as e:
            LOGGER.error(f"Gradient chat call failed: {e}")
            raise

        # Save conversation history
        if conversation_id:
            hist = self.conversations.setdefault(conversation_id, [])
            hist.append({"role": "user", "text": query})
            hist.append({"role": "assistant", "text": answer})
            if len(hist) > 30:
                self.conversations[conversation_id] = hist[-30:]

        return answer
