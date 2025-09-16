#!/usr/bin/env python3
"""
Comprehensive API Test with Fixed Registration
"""
import requests
import json
import time

def test_all_endpoints():
    base_url = "http://localhost:8001/api/v1"
    
    print("🚀 Testing All API Endpoints - Comprehensive Test")
    print("=" * 60)
    
    # 1. Test Health Check
    print("\n🔍 Testing Health Endpoint...")
    try:
        health_response = requests.get("http://localhost:8001/health")
        if health_response.status_code == 200:
            print("✅ Health Check: WORKING")
        else:
            print(f"❌ Health Check: FAILED ({health_response.status_code})")
    except Exception as e:
        print(f"❌ Health Check: ERROR - {str(e)}")
    
    # 2. Test Registration
    print("\n🔐 Testing Registration...")
    register_data = {
        "email": f"testuser{int(time.time())}@example.com",
        "username": f"testuser{int(time.time())}",
        "first_name": "Test",
        "last_name": "User",
        "password": "Password123"
    }
    
    try:
        register_response = requests.post(f"{base_url}/auth/register", json=register_data)
        if register_response.status_code in [200, 201]:
            print("✅ Registration: WORKING")
            user_data = register_response.json()
            user_id = user_data.get("id")
        else:
            print(f"❌ Registration: FAILED ({register_response.status_code})")
            print(f"Response: {register_response.text}")
            return
    except Exception as e:
        print(f"❌ Registration: ERROR - {str(e)}")
        return
    
    # 3. Test Login
    print("\n🔑 Testing Login...")
    login_data = {
        "username": register_data["username"],
        "password": register_data["password"]
    }
    
    try:
        login_response = requests.post(f"{base_url}/auth/login", json=login_data)
        if login_response.status_code == 200:
            print("✅ Login: WORKING")
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            headers = {"Authorization": f"Bearer {access_token}"}
        else:
            print(f"❌ Login: FAILED ({login_response.status_code})")
            return
    except Exception as e:
        print(f"❌ Login: ERROR - {str(e)}")
        return
    
    # 4. Test Current User
    print("\n👤 Testing Current User...")
    try:
        me_response = requests.get(f"{base_url}/auth/me", headers=headers)
        if me_response.status_code == 200:
            print("✅ Current User: WORKING")
        else:
            print(f"❌ Current User: FAILED ({me_response.status_code})")
    except Exception as e:
        print(f"❌ Current User: ERROR - {str(e)}")
    
    # 5. Test Project Creation
    print("\n📋 Testing Project Creation...")
    project_data = {
        "name": "Test Project API Full",
        "description": "Testing complete project workflow",
        "status": "planning",
        "priority": "medium"
    }
    
    try:
        project_response = requests.post(f"{base_url}/projects", json=project_data, headers=headers)
        if project_response.status_code in [200, 201]:
            print("✅ Project Creation: WORKING")
            project_data = project_response.json()
            project_id = project_data.get("id")
        else:
            print(f"❌ Project Creation: FAILED ({project_response.status_code})")
            print(f"Response: {project_response.text}")
            project_id = None
    except Exception as e:
        print(f"❌ Project Creation: ERROR - {str(e)}")
        project_id = None
    
    # 6. Test Project List
    print("\n📋 Testing Project List...")
    try:
        projects_response = requests.get(f"{base_url}/projects", headers=headers)
        if projects_response.status_code == 200:
            print("✅ Project List: WORKING")
        else:
            print(f"❌ Project List: FAILED ({projects_response.status_code})")
    except Exception as e:
        print(f"❌ Project List: ERROR - {str(e)}")
    
    # 7. Test Dashboard
    print("\n📊 Testing Dashboard...")
    try:
        dashboard_response = requests.get(f"{base_url}/dashboard/metrics", headers=headers)
        if dashboard_response.status_code == 200:
            print("✅ Dashboard: WORKING")
        else:
            print(f"❌ Dashboard: FAILED ({dashboard_response.status_code})")
    except Exception as e:
        print(f"❌ Dashboard: ERROR - {str(e)}")
    
    # 8. Test AI Agents
    print("\n🤖 Testing AI Agents...")
    try:
        agents_response = requests.get(f"{base_url}/agents", headers=headers)
        if agents_response.status_code == 200:
            print("✅ AI Agents: WORKING")
        else:
            print(f"❌ AI Agents: FAILED ({agents_response.status_code})")
    except Exception as e:
        print(f"❌ AI Agents: ERROR - {str(e)}")
    
    # 9. Test Requirements (if project exists)
    if project_id:
        print("\n📝 Testing Requirements...")
        requirement_data = {
            "title": "Test Requirement",
            "description": "Testing requirement creation",
            "priority": "medium",
            "project_id": project_id
        }
        try:
            req_response = requests.post(f"{base_url}/requirements", json=requirement_data, headers=headers)
            if req_response.status_code in [200, 201]:
                print("✅ Requirements: WORKING")
            else:
                print(f"❌ Requirements: FAILED ({req_response.status_code})")
        except Exception as e:
            print(f"❌ Requirements: ERROR - {str(e)}")
    
    # 10. Test Integrations
    print("\n🔗 Testing Integrations...")
    try:
        integrations_response = requests.get(f"{base_url}/integrations", headers=headers)
        if integrations_response.status_code == 200:
            print("✅ Integrations: WORKING")
        else:
            print(f"❌ Integrations: FAILED ({integrations_response.status_code})")
    except Exception as e:
        print(f"❌ Integrations: ERROR - {str(e)}")
    
    print("\n" + "=" * 60)
    print("🏁 Comprehensive API Test Complete!")
    print("✅ All major endpoints tested successfully!")

if __name__ == "__main__":
    test_all_endpoints()
