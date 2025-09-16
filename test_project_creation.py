#!/usr/bin/env python3
"""
Test script for project creation debugging
"""
import requests
import json

def test_project_creation():
    base_url = "http://localhost:8000/api/v1"
    
    # 1. Test login
    print("🔑 Testing login...")
    login_data = {
        "username": "testuser",
        "password": "Password123"
    }
    
    try:
        login_response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Login Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print("✅ Login successful!")
            print(f"Token received: {access_token[:20]}..." if access_token else "No token received")
            
            # 2. Test project creation
            print("\n📝 Testing project creation...")
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            project_data = {
                "name": "Test Project",
                "description": "A test project for debugging",
                "status": "planning",
                "priority": "medium"
            }
            
            project_response = requests.post(f"{base_url}/projects/", json=project_data, headers=headers)
            print(f"Project Creation Status: {project_response.status_code}")
            
            if project_response.status_code == 201:
                project_result = project_response.json()
                print("✅ Project created successfully!")
                print(f"Project ID: {project_result.get('id')}")
                print(f"Project Name: {project_result.get('name')}")
            else:
                print("❌ Project creation failed!")
                print(f"Response: {project_response.text}")
                
        else:
            print("❌ Login failed!")
            print(f"Response: {login_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Is the server running on port 8000?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_project_creation()
