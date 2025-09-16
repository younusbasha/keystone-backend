#!/usr/bin/env python3
"""
Comprehensive API Endpoint Testing Script
"""
import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, headers=None, expected_status=None):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)

        status = "✅ PASS" if response.status_code < 400 else "❌ FAIL"
        print(f"{status} {method} {endpoint} - Status: {response.status_code}")

        if response.status_code < 400:
            try:
                result = response.json()
                if isinstance(result, dict) and len(str(result)) < 200:
                    print(f"     Response: {result}")
            except:
                if len(response.text) < 100:
                    print(f"     Response: {response.text}")
        else:
            print(f"     Error: {response.text[:100]}...")

        return response.status_code < 400
    except Exception as e:
        print(f"❌ ERROR {method} {endpoint} - Exception: {str(e)}")
        return False

def main():
    print("🚀 Testing TechSophy Keystone API Endpoints")
    print("=" * 50)

    # Test basic endpoints
    print("\n📋 Testing Basic Endpoints:")
    test_endpoint("GET", "/")
    test_endpoint("GET", "/health")
    test_endpoint("GET", "/docs")
    test_endpoint("GET", "/redoc")

    # Test API v1 endpoints
    print("\n📋 Testing API v1 Endpoints:")
    test_endpoint("GET", "/api/v1/")
    test_endpoint("GET", "/api/v1/users/")
    test_endpoint("GET", "/api/v1/projects/")
    test_endpoint("GET", "/api/v1/requirements/")
    test_endpoint("GET", "/api/v1/tasks/")
    test_endpoint("GET", "/api/v1/agents/")

    # Test user registration (should work without auth)
    print("\n👤 Testing User Registration:")
    test_user_data = {
        "email": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
        "username": f"testuser_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "first_name": "Test",
        "last_name": "User",
        "password": "TestPassword123!"
    }

    register_success = test_endpoint("POST", "/api/v1/auth/register", test_user_data)

    if register_success:
        print("\n🔐 Testing User Login:")
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        test_endpoint("POST", "/api/v1/auth/login", login_data)

    # Test protected endpoints (might require auth)
    print("\n🔒 Testing Protected Endpoints (may require auth):")
    test_endpoint("GET", "/api/v1/users/me")
    test_endpoint("GET", "/api/v1/dashboard/stats")

    print("\n" + "=" * 50)
    print("✅ API Endpoint Testing Complete!")
    print("\n💡 If you see ❌ FAIL status codes:")
    print("   - 401/403: Authentication required (normal for protected endpoints)")
    print("   - 404: Endpoint not found (check route configuration)")
    print("   - 500: Server error (check application logs)")
    print(f"\n🌐 Access your API documentation at: {BASE_URL}/docs")

if __name__ == "__main__":
    main()
