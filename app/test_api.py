#!/usr/bin/env python3

import requests
import json

def test_chat_endpoint():
    """Test the /chat endpoint"""
    url = "http://localhost:8000/chat"
    
    # Test message
    data = {
        "message": "Hello! Can you tell me about event planning?"
    }
    
    try:
        print("Testing chat endpoint...")
        response = requests.post(url, json=data, timeout=60)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            try:
                json_response = response.json()
                print("✅ Chat endpoint working!")
                print(f"Bot response: {json_response.get('response', 'No response field')}")
            except json.JSONDecodeError:
                print("⚠️ Response is not valid JSON")
        else:
            print(f"❌ Chat endpoint failed with status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

def test_health_endpoint():
    """Test the health endpoint"""
    url = "http://localhost:8000/"
    
    try:
        print("\nTesting health endpoint...")
        response = requests.get(url, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Health endpoint working!")
        else:
            print(f"❌ Health endpoint failed with status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_health_endpoint()
    test_chat_endpoint()