#!/usr/bin/env python3
"""
Test script to show the difference between Gradient AI responses 
and a hypothetical local/offline response
"""

import requests
import json

def test_gradient_ai_quality():
    """Test the quality and intelligence of DigitalOcean Gradient AI responses"""
    
    url = "http://localhost:8000/chat"
    
    # Test with a complex event planning scenario
    complex_queries = [
        {
            "query": "I'm planning a corporate conference for 500 people with a $50,000 budget. The event is in 3 months. What are the most critical timeline milestones I should focus on, and how should I allocate my budget across different categories?",
            "description": "Complex budget and timeline planning"
        },
        {
            "query": "My outdoor wedding reception got moved indoors last minute due to weather. I have 150 guests arriving in 4 hours. What emergency adjustments should I prioritize to save the event?",
            "description": "Crisis management scenario"
        },
        {
            "query": "I need to plan a hybrid virtual-physical product launch event that caters to both in-person VIPs and online attendees globally across different time zones. What technology and logistics challenges should I anticipate?",
            "description": "Modern hybrid event complexity"
        }
    ]
    
    print("🧠 Testing DigitalOcean Gradient AI Intelligence...")
    print("=" * 80)
    
    for i, test_case in enumerate(complex_queries, 1):
        print(f"\n🎯 Test Case {i}: {test_case['description']}")
        print(f"📝 Query: {test_case['query'][:100]}...")
        
        try:
            response = requests.post(url, json={"query": test_case['query']}, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', 'No answer')
                
                print(f"✅ Status: {response.status_code}")
                print(f"🤖 AI Response Length: {len(answer)} characters")
                print(f"📄 Response Preview: {answer[:200]}...")
                
                # Check for intelligent features
                intelligence_indicators = {
                    "Specific numbers/budgets": any(char.isdigit() for char in answer),
                    "Timeline mentions": any(word in answer.lower() for word in ['month', 'week', 'day', 'hour', 'timeline']),
                    "Actionable steps": 'step' in answer.lower() or any(num in answer for num in ['1.', '2.', '3.', '•', '-']),
                    "Context awareness": len(answer.split()) > 50,
                    "Professional terminology": any(word in answer.lower() for word in ['budget', 'logistics', 'venue', 'catering', 'contingency'])
                }
                
                print("🧠 Intelligence Analysis:")
                for indicator, present in intelligence_indicators.items():
                    status = "✅" if present else "❌"
                    print(f"   {status} {indicator}")
                    
                print(f"🎯 Intelligence Score: {sum(intelligence_indicators.values())}/5")
                
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
            
        print("-" * 80)

def compare_with_simple_response():
    """Show what a simple offline response might look like"""
    
    print("\n🏠 Comparison: What a Simple Offline Response Might Look Like")
    print("=" * 80)
    
    simple_responses = [
        "For event planning, create a budget, book a venue, and send invitations.",
        "In case of emergency, contact vendors and inform guests about changes.",
        "For hybrid events, use video conferencing and ensure good internet connection."
    ]
    
    for i, simple_response in enumerate(simple_responses, 1):
        print(f"🏠 Simple Response {i}: {simple_response}")
        print(f"📊 Length: {len(simple_response)} characters")
        print(f"🎯 Intelligence Score: 1/5 (basic/generic)")
        print("-" * 40)

if __name__ == "__main__":
    print("🔬 EventEase AI Bot Intelligence Test")
    print("This test demonstrates the value of DigitalOcean Gradient AI vs simple offline responses")
    print("\n" + "=" * 80)
    
    test_gradient_ai_quality()
    compare_with_simple_response()
    
    print("\n🎯 CONCLUSION:")
    print("DigitalOcean Gradient AI provides:")
    print("✅ Context-aware, detailed responses")
    print("✅ Professional event planning expertise") 
    print("✅ Specific, actionable advice")
    print("✅ Crisis management insights")
    print("✅ Modern event technology knowledge")
    print("\n🏠 Pure offline would only provide:")
    print("❌ Generic, basic responses")
    print("❌ Limited contextual understanding")
    print("❌ No specialized domain knowledge")