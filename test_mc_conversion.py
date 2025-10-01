#!/usr/bin/env python3
"""
Test MC number conversion functionality
"""
import requests
import json

# Test data - different formats of MC numbers
test_cases = [
    {"mc_number": "123456"},      # String
    {"mc_number": 123456},        # Integer
    {"mc_number": 123456.0},      # Float
    {"mc_number": "MC-123456"},   # String with prefix
    {"mc_number": "MC 123456"},   # String with prefix and space
]

API_URL = "http://localhost:8000"
API_KEY = "your-api-key"  # Replace with actual API key

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def test_verify_mc_endpoint():
    """Test the /verify_mc endpoint with different MC number formats"""
    print("🧪 Testing MC Number Conversion in /verify_mc endpoint\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: MC Number = {test_case['mc_number']} (type: {type(test_case['mc_number']).__name__})")
        
        try:
            response = requests.post(
                f"{API_URL}/verify_mc",
                headers=headers,
                json=test_case,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success: {result.get('mc_number')} - Eligible: {result.get('eligible')}")
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("-" * 50)

def test_webhook_endpoint():
    """Test the /webhook/happyrobot endpoint with different MC number formats"""
    print("\n🧪 Testing MC Number Conversion in /webhook/happyrobot endpoint\n")
    
    webhook_test_cases = [
        {
            "mc_number": 123456,
            "equipment_type": "Dry Van",
            "origin": "Chicago, IL",
            "destination": "Dallas, TX",
            "initial_offer": 2100
        },
        {
            "mc_number": "654321",
            "equipment_type": "Refrigerated",
            "origin": "Los Angeles, CA", 
            "destination": "Phoenix, AZ",
            "initial_offer": 1800
        }
    ]
    
    for i, test_case in enumerate(webhook_test_cases, 1):
        print(f"Webhook Test {i}: MC Number = {test_case['mc_number']} (type: {type(test_case['mc_number']).__name__})")
        
        try:
            response = requests.post(
                f"{API_URL}/webhook/happyrobot",
                json=test_case,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success: Status = {result.get('status')}")
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("-" * 50)

if __name__ == "__main__":
    print("🚀 Starting MC Number Conversion Tests")
    print("=" * 60)
    
    # Test verify_mc endpoint
    test_verify_mc_endpoint()
    
    # Test webhook endpoint  
    test_webhook_endpoint()
    
    print("\n✅ Tests completed!")