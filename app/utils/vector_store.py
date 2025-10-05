# app/utils/vector_store.py
import os
import pickle
from typing import List, Dict
from utils.config import settings
import numpy as np
import requests
import math
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

# Lazy import of sentence-transformers / openai to avoid heavy imports if not needed
_sentence_transformer = None
_openai = None

def _ensure_sentence_transformer(model_name: str):
    global _sentence_transformer
    if _sentence_transformer is None:
        from sentence_transformers import SentenceTransformer
        _sentence_transformer = SentenceTransformer(model_name)
    return _sentence_transformer

def _ensure_openai():
    global _openai
    if _openai is None:
        try:
            import openai as _o
            _openai = _o
        except Exception:
            _openai = None
    return _openai

class VectorStore:
    def __init__(self, vector_dir: str):
        self.vector_dir = vector_dir
        os.makedirs(self.vector_dir, exist_ok=True)
        self.index_path = os.path.join(self.vector_dir, "vs_index.pkl")
        # default (sentence-transformers) model name kept for fallback
        self.emb_model_name = getattr(settings, "EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
        # batch size for embeddings requests
        self.batch_size = getattr(settings, "EMBEDDING_BATCH_SIZE", 32)
        # internal doc store: list of {"id","text","meta","emb"}
        self._docs: List[Dict] = []
        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, "rb") as f:
                    self._docs = pickle.load(f)
            except Exception as e:
                LOGGER.warning("Could not load existing vector index: %s", e)
                self._docs = []

    def persist(self):
        with open(self.index_path, "wb") as f:
            pickle.dump(self._docs, f)

    def _call_gradient_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Call Gradient's OpenAI-compatible embeddings endpoint:
        POST {GRADIENT_API_BASE}/v1/embeddings
        payload: {"model": <model>, "input": texts}
        """
        api_key = getattr(settings, "GRADIENT_API_KEY", None) or os.getenv("GRADIENT_API_KEY")
        base = getattr(settings, "GRADIENT_API_BASE", None) or os.getenv("GRADIENT_API_BASE", "https://inference.do-ai.run")
        model = getattr(settings, "GRADIENT_EMBEDDING_MODEL", None) or os.getenv("GRADIENT_EMBEDDING_MODEL")

        if not api_key or not model:
            raise RuntimeError("Gradient embeddings not configured (GRADIENT_API_KEY or GRADIENT_EMBEDDING_MODEL missing).")

        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        # Use only DigitalOcean Gradient AI endpoint
        base_candidates = [
            base.rstrip("/"),
        ]
        payload = {"model": model, "input": texts}

        last_error = None
        for b in base_candidates:
            url = f"{b}/v1/embeddings"
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=30)
                if resp.status_code != 200:
                    LOGGER.warning(
                        "Gradient embeddings non-200 (%d) at %s: %s",
                        resp.status_code,
                        url,
                        resp.text[:500],
                    )
                    resp.raise_for_status()
                data = resp.json()
                embeddings = [item["embedding"] for item in data.get("data", [])]
                return embeddings
            except Exception as e:
                last_error = e
                LOGGER.warning("Gradient embeddings endpoint failed (%s): %s", url, e)
                continue
        raise RuntimeError(f"All Gradient embeddings endpoints failed: {last_error}")

    def _call_openai_embeddings(self, texts: List[str]) -> List[List[float]]:
        openai = _ensure_openai()
        openai_api_key = getattr(settings, "OPENAI_API_KEY", None) or os.getenv("OPENAI_API_KEY")
        model = getattr(settings, "OPENAI_EMBEDDING_MODEL", None) or os.getenv("OPENAI_EMBEDDING_MODEL")
        if openai is None or not openai_api_key or not model:
            raise RuntimeError("OpenAI embeddings not available or not configured.")
        openai.api_key = openai_api_key
        # OpenAI supports batching; we'll call with list
        resp = openai.Embedding.create(model=model, input=texts)
        embeddings = [d["embedding"] for d in resp["data"]]
        return embeddings

    def _call_sentence_transformers(self, texts: List[str]) -> List[List[float]]:
        model = _ensure_sentence_transformer(self.emb_model_name)
        embs = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return [e.tolist() for e in embs]

    def _embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embed texts using local sentence-transformers since DigitalOcean Gradient AI 
        doesn't support embeddings endpoints.
        """
        all_embs: List[List[float]] = []
        
        # Try Gradient embeddings first (but it will likely fail with DigitalOcean)
        use_gradient_flag = (
            getattr(settings, "USE_GRADIENT_EMBEDDINGS", False)
            or os.getenv("USE_GRADIENT_EMBEDDINGS", "false").lower() in ("1", "true", "yes")
        )
        
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            
            if use_gradient_flag:
                try:
                    emb_batch = self._call_gradient_embeddings(batch)
                    LOGGER.info("Embedded batch using Gradient (size=%d).", len(batch))
                    all_embs.extend(emb_batch)
                    continue
                except Exception as e:
                    LOGGER.error("Gradient embeddings failed: %s", e)
                    LOGGER.info("Falling back to sentence-transformers for this batch")
            
            # Use sentence-transformers as fallback (or primary if Gradient disabled)
            try:
                emb_batch = self._call_sentence_transformers(batch)
                LOGGER.info("Embedded batch using sentence-transformers (size=%d).", len(batch))
                all_embs.extend(emb_batch)
            except Exception as e:
                LOGGER.error("Sentence-transformers embeddings failed: %s", e)
                raise RuntimeError(f"All embedding methods failed: {e}")
                
        return all_embs

    def add_documents(self, docs: List[Dict], override: bool = False):
        """
        docs: list of {"id","text","meta"}
        This will embed docs.text using the configured embeddings provider.
        """
        if override:
            self._docs = []

        texts = [d["text"] for d in docs]
        # get embeddings
        embs = self._embed_texts(texts)  # list of lists

        for d, emb in zip(docs, embs):
            item = {"id": d["id"], "text": d["text"], "meta": d.get("meta", {}), "emb": np.array(emb, dtype=np.float32)}
            self._docs.append(item)

        self.persist()
        LOGGER.info("Added %d documents to vector store (total=%d).", len(docs), len(self._docs))

    def similarity_search(self, query: str, k: int = 4):
        """
        Return top-k nearest docs by cosine similarity.
        """
        if not self._docs:
            return []
        # embed query
        q_emb_list = self._embed_texts([query])
        q_emb = np.array(q_emb_list[0], dtype=np.float32)

        embs = np.vstack([d["emb"] for d in self._docs])
        # cosine similarity
        q_norm = np.linalg.norm(q_emb) + 1e-12
        doc_norms = np.linalg.norm(embs, axis=1) + 1e-12
        sims = (embs @ q_emb) / (doc_norms * q_norm)
        idxs = np.argsort(sims)[::-1][:k]
        results = []
        for i in idxs:
            d = self._docs[int(i)]
            results.append({"id": d["id"], "text": d["text"], "meta": d["meta"], "score": float(sims[int(i)])})
        return results
