# app/utils/loader.py
from typing import List, Dict
from pathlib import Path
import os
from PyPDF2 import PdfReader
import uuid
import re
from utils.config import settings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_pdf_text(pdf_path: str) -> str:
    """Extract raw text from PDF file."""
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def load_text_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def chunk_text(text: str, max_tokens: int = 400, overlap_tokens: int = 40) -> List[str]:
    """
    Split text into token-aware chunks.
    Uses LangChain's RecursiveCharacterTextSplitter
    tuned roughly to ~400 tokens (~1500 chars) with overlap.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_tokens * 4,  # rough char equivalent
        chunk_overlap=overlap_tokens * 4,
        length_function=len,
        separators=["\n\n", "\n", ".", "!", "?", " "]
    )
    return splitter.split_text(text)

def prepare_docs_from_file(file_path: str) -> List[Dict]:
    """
    Load, split, and structure docs for ingestion.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        raw = load_pdf_text(file_path)
    else:
        raw = load_text_file(file_path)

    chunks = chunk_text(raw)
    docs = [{"id": f"{os.path.basename(file_path)}_{i}", "text": c, "meta": {"source": os.path.basename(file_path)}} for i, c in enumerate(chunks)]
    return docs

def load_document_chunks(file_path: str) -> List[Dict]:
    """
    Alias for prepare_docs_from_file for backward compatibility.
    """
    return prepare_docs_from_file(file_path)
