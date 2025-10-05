#!/usr/bin/env python3

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_file_upload():
    """Test the /ingest endpoint with a simple text file"""
    
    # Create a simple test file
    test_content = """
    Event Planning Best Practices
    
    1. Set clear objectives and goals
    2. Create a detailed timeline and budget
    3. Choose the right venue for your event
    4. Plan catering and entertainment
    5. Send invitations early
    6. Prepare for contingencies
    7. Follow up after the event
    
    These are fundamental steps for successful event planning.
    """
    
    test_file_path = "test_event_planning.txt"
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    # Test the ingest endpoint
    url = "http://localhost:8000/ingest"
    
    try:
        print("Testing file upload to /ingest endpoint...")
        
        with open(test_file_path, "rb") as f:
            files = {"file": (test_file_path, f, "text/plain")}
            response = requests.post(f"{url}?override=true", files=files, timeout=60)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ File upload successful!")
            try:
                json_response = response.json()
                print(f"Response: {json_response}")
            except:
                print("Response is not JSON format")
        else:
            print(f"❌ File upload failed with status {response.status_code}")
            
        # Clean up test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

def test_chat_with_context():
    """Test chat endpoint after file upload"""
    
    url = "http://localhost:8000/chat"
    
    data = {
        "query": "What are the best practices for event planning?"
    }
    
    try:
        print("\nTesting chat with uploaded context...")
        response = requests.post(url, json=data, timeout=60)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            try:
                json_response = response.json()
                print("✅ Chat with context working!")
                print(f"Bot response: {json_response.get('answer', 'No answer field')}")
            except:
                print("Response is not JSON format")
        else:
            print(f"❌ Chat failed with status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing EventEase AI Bot functionality...")
    test_file_upload()
    test_chat_with_context()