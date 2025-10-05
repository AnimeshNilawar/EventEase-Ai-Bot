# Test DigitalOcean Gradient AI Serverless Inference
import os
import requests
from utils.config import settings

# Load environment variables
GRADIENT_API_KEY = os.getenv("GRADIENT_API_KEY", "sk-do-r04zQMwB2XKw8sGhz3KVInBgzlGNpM5uladGkofoJv2Xmasf3dwwIuw3cE")
GRADIENT_API_BASE = os.getenv("GRADIENT_API_BASE", "https://inference.do-ai.run")

print(f"Testing DigitalOcean Gradient AI Serverless Inference...")
print(f"API Base: {GRADIENT_API_BASE}")
print(f"API Key: ***{GRADIENT_API_KEY[-4:] if GRADIENT_API_KEY else 'NOT SET'}")

# Test the official DigitalOcean endpoint
endpoint = f"{GRADIENT_API_BASE}/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GRADIENT_API_KEY}",
    "Content-Type": "application/json",
}

# Test payload according to DigitalOcean Gradient AI documentation
test_payload = {
    "model": "llama3.3-70b-instruct",
    "messages": [
        {"role": "user", "content": "What is the capital of France?"}
    ],
    "temperature": 0.7,
    "max_tokens": 50
}

print(f"\n🧪 Testing DigitalOcean Gradient AI endpoint: {endpoint}")

try:
    print("   📡 Sending request...")
    response = requests.post(endpoint, headers=headers, json=test_payload, timeout=30)
    print(f"   📊 Status Code: {response.status_code}")
    print(f"   📋 Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"   ✅ JSON Response: {data}")
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0].get("message", {}).get("content", "")
                print(f"   🎉 SUCCESS! Response: {content}")
            else:
                print(f"   ⚠️  Unexpected format: {data}")
        except ValueError as e:
            print(f"   ❌ JSON Parse Error: {e}")
            print(f"   📄 Raw Response: {response.text[:500]}")
    else:
        print(f"   ❌ Error Status: {response.status_code}")
        print(f"   📄 Error Response: {response.text[:500]}")
        
except requests.exceptions.RequestException as e:
    print(f"   ❌ Request Failed: {e}")
except Exception as e:
    print(f"   ❌ Unexpected Error: {e}")

print("\n" + "="*50)
print("DigitalOcean Gradient AI test completed.")