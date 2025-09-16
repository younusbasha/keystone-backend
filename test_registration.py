#!/usr/bin/env python3
"""
Test script for registration and authentication debugging
"""
import requests
import json

def test_full_flow():
    base_url = "http://localhost:8000/api/v1"

    # 1. Test registration first
    print("📝 Testing user registration...")
    register_data = {
        "email": "debuguser@example.com",
        "username": "debuguser",
        "first_name": "Debug",
        "last_name": "User",
        "password": "Password123"
    }

    try:
        register_response = requests.post(f"{base_url}/auth/register", json=register_data)
        print(f"Registration Status: {register_response.status_code}")

        if register_response.status_code in [200, 201]:
            print("✅ Registration successful!")
            user_data = register_response.json()
            print(f"User created: {user_data}")
        else:
            print("❌ Registration failed!")
            print(f"Response: {register_response.text}")

        # 2. Test login with newly created user
        print("\n🔑 Testing login with new user...")
        login_data = {
            "username": "debuguser",
            "password": "Password123"
        }

        login_response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Login Status: {login_response.status_code}")

        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print("✅ Login successful!")
            print(f"Token received: {access_token[:20]}..." if access_token else "No token received")

            # 3. Test project creation
            print("\n📝 Testing project creation...")
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            project_data = {
                "name": "Debug Test Project",
                "description": "A test project for debugging project creation",
                "status": "planning",
                "priority": "medium"
            }

            project_response = requests.post(f"{base_url}/projects/", json=project_data, headers=headers)
            print(f"Project Creation Status: {project_response.status_code}")

            if project_response.status_code == 201:
                project_result = project_response.json()
                print("✅ Project created successfully!")
                print(f"Project Details: {json.dumps(project_result, indent=2)}")
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
    test_full_flow()
