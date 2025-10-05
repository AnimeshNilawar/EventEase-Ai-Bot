#!/usr/bin/env python3

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gradient_embeddings():
    """Test DigitalOcean Gradient AI embeddings endpoint"""
    
    api_key = os.getenv("GRADIENT_API_KEY")
    if not api_key:
        print("❌ GRADIENT_API_KEY not found in environment")
        return
    
    # DigitalOcean Gradient AI endpoint
    url = "https://inference.do-ai.run/v1/embeddings"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test payload
    payload = {
        "model": "text-embedding-ada-002",  # Try a standard embedding model
        "input": ["Hello world", "Test text for embeddings"]
    }
    
    try:
        print("Testing DigitalOcean Gradient AI embeddings...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response: {response.text[:500]}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Embeddings endpoint working!")
            print(f"Number of embeddings returned: {len(data.get('data', []))}")
        else:
            print(f"❌ Embeddings failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_available_models():
    """Test what models are available"""
    
    api_key = os.getenv("GRADIENT_API_KEY")
    if not api_key:
        print("❌ GRADIENT_API_KEY not found in environment")
        return
    
    # Try to get available models
    url = "https://inference.do-ai.run/v1/models"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        print("\nTesting available models...")
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:1000]}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Models endpoint working!")
            models = data.get('data', [])
            print(f"Available models: {len(models)}")
            for model in models[:5]:  # Show first 5 models
                print(f"  - {model.get('id', 'unknown')}")
        else:
            print(f"❌ Models failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_available_models()
    test_gradient_embeddings()