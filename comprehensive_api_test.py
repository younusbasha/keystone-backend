#!/usr/bin/env python3
"""
Comprehensive API Endpoint Testing Script
Tests all endpoints in the TechSophy Keystone backend
"""
import requests
import json
import time
from datetime import datetime, timedelta

class APITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api/v1"
        self.access_token = None
        self.test_user_id = None
        self.test_project_id = None
        self.test_requirement_id = None
        self.test_task_id = None
        self.test_agent_id = None
        
    def log_test(self, test_name, status, response_code=None, message=""):
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        code_info = f" [{response_code}]" if response_code else ""
        print(f"{status_icon} {test_name}{code_info} - {message}")
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        print("\n🔍 Testing Health Endpoint")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Check", "PASS", response.status_code, f"Service: {data.get('service', 'Unknown')}")
                return True
            else:
                self.log_test("Health Check", "FAIL", response.status_code, response.text)
                return False
        except Exception as e:
            self.log_test("Health Check", "FAIL", None, str(e))
            return False
    
    def test_auth_endpoints(self):
        """Test authentication endpoints"""
        print("\n🔐 Testing Authentication Endpoints")
        
        # Test user registration
        register_data = {
            "email": f"testuser_{int(time.time())}@example.com",
            "username": f"testuser_{int(time.time())}",
            "first_name": "Test",
            "last_name": "User",
            "password": "Password123"
        }
        
        try:
            response = requests.post(f"{self.api_base}/auth/register", json=register_data)
            if response.status_code == 201:
                user_data = response.json()
                self.test_user_id = user_data.get("id")
                self.log_test("User Registration", "PASS", response.status_code, f"User ID: {self.test_user_id}")
            else:
                self.log_test("User Registration", "FAIL", response.status_code, response.text)
                return False
        except Exception as e:
            self.log_test("User Registration", "FAIL", None, str(e))
            return False
        
        # Test user login
        login_data = {
            "username": register_data["username"],
            "password": register_data["password"]
        }
        
        try:
            response = requests.post(f"{self.api_base}/auth/login", json=login_data)
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                self.log_test("User Login", "PASS", response.status_code, "Token received")
                return True
            else:
                self.log_test("User Login", "FAIL", response.status_code, response.text)
                return False
        except Exception as e:
            self.log_test("User Login", "FAIL", None, str(e))
            return False
    
    def get_auth_headers(self):
        """Get authorization headers"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def test_project_endpoints(self):
        """Test project management endpoints"""
        print("\n📋 Testing Project Endpoints")
        
        if not self.access_token:
            self.log_test("Project Endpoints", "SKIP", None, "No auth token available")
            return False
        
        headers = self.get_auth_headers()
        
        # Test project creation
        project_data = {
            "name": "Test Project",
            "description": "A test project for API testing",
            "status": "planning",
            "priority": "medium"
        }
        
        try:
            response = requests.post(f"{self.api_base}/projects/", json=project_data, headers=headers)
            if response.status_code == 201:
                project = response.json()
                self.test_project_id = project.get("id")
                self.log_test("Project Creation", "PASS", response.status_code, f"Project ID: {self.test_project_id}")
            else:
                self.log_test("Project Creation", "FAIL", response.status_code, response.text)
                return False
        except Exception as e:
            self.log_test("Project Creation", "FAIL", None, str(e))
            return False
        
        # Test get projects
        try:
            response = requests.get(f"{self.api_base}/projects/", headers=headers)
            if response.status_code == 200:
                projects = response.json()
                self.log_test("Get Projects", "PASS", response.status_code, f"Found {projects.get('total', 0)} projects")
            else:
                self.log_test("Get Projects", "FAIL", response.status_code, response.text)
        except Exception as e:
            self.log_test("Get Projects", "FAIL", None, str(e))
        
        # Test get single project
        if self.test_project_id:
            try:
                response = requests.get(f"{self.api_base}/projects/{self.test_project_id}", headers=headers)
                if response.status_code == 200:
                    self.log_test("Get Single Project", "PASS", response.status_code, "Project details retrieved")
                else:
                    self.log_test("Get Single Project", "FAIL", response.status_code, response.text)
            except Exception as e:
                self.log_test("Get Single Project", "FAIL", None, str(e))
        
        # Test project update
        if self.test_project_id:
            update_data = {"description": "Updated project description"}
            try:
                response = requests.put(f"{self.api_base}/projects/{self.test_project_id}", json=update_data, headers=headers)
                if response.status_code == 200:
                    self.log_test("Project Update", "PASS", response.status_code, "Project updated successfully")
                else:
                    self.log_test("Project Update", "FAIL", response.status_code, response.text)
            except Exception as e:
                self.log_test("Project Update", "FAIL", None, str(e))
        
        return True
    
    def test_requirement_endpoints(self):
        """Test requirement management endpoints"""
        print("\n📝 Testing Requirement Endpoints")
        
        if not self.access_token or not self.test_project_id:
            self.log_test("Requirement Endpoints", "SKIP", None, "No auth token or project ID available")
            return False
        
        headers = self.get_auth_headers()
        
        # Test requirement creation
        requirement_data = {
            "title": "Test Requirement",
            "description": "A test requirement for the API",
            "priority": "high",
            "complexity": "medium",
            "project_id": self.test_project_id
        }
        
        try:
            response = requests.post(f"{self.api_base}/requirements/", json=requirement_data, headers=headers)
            if response.status_code == 201:
                requirement = response.json()
                self.test_requirement_id = requirement.get("id")
                self.log_test("Requirement Creation", "PASS", response.status_code, f"Requirement ID: {self.test_requirement_id}")
            else:
                self.log_test("Requirement Creation", "FAIL", response.status_code, response.text)
                return False
        except Exception as e:
            self.log_test("Requirement Creation", "FAIL", None, str(e))
            return False
        
        # Test get requirements
        try:
            response = requests.get(f"{self.api_base}/requirements/", headers=headers)
            if response.status_code == 200:
                self.log_test("Get Requirements", "PASS", response.status_code, "Requirements retrieved")
            else:
                self.log_test("Get Requirements", "FAIL", response.status_code, response.text)
        except Exception as e:
            self.log_test("Get Requirements", "FAIL", None, str(e))
        
        return True
    
    def test_task_endpoints(self):
        """Test task management endpoints"""
        print("\n✅ Testing Task Endpoints")
        
        if not self.access_token or not self.test_project_id:
            self.log_test("Task Endpoints", "SKIP", None, "No auth token or project ID available")
            return False
        
        headers = self.get_auth_headers()
        
        # Test task creation
        task_data = {
            "title": "Test Task",
            "description": "A test task for the API",
            "priority": "high",
            "status": "todo",
            "estimated_hours": 8,
            "project_id": self.test_project_id
        }
        
        try:
            response = requests.post(f"{self.api_base}/tasks/", json=task_data, headers=headers)
            if response.status_code == 201:
                task = response.json()
                self.test_task_id = task.get("id")
                self.log_test("Task Creation", "PASS", response.status_code, f"Task ID: {self.test_task_id}")
            else:
                self.log_test("Task Creation", "FAIL", response.status_code, response.text)
                return False
        except Exception as e:
            self.log_test("Task Creation", "FAIL", None, str(e))
            return False
        
        # Test get tasks
        try:
            response = requests.get(f"{self.api_base}/tasks/", headers=headers)
            if response.status_code == 200:
                self.log_test("Get Tasks", "PASS", response.status_code, "Tasks retrieved")
            else:
                self.log_test("Get Tasks", "FAIL", response.status_code, response.text)
        except Exception as e:
            self.log_test("Get Tasks", "FAIL", None, str(e))
        
        return True
    
    def test_agent_endpoints(self):
        """Test AI agent endpoints"""
        print("\n🤖 Testing AI Agent Endpoints")
        
        if not self.access_token:
            self.log_test("Agent Endpoints", "SKIP", None, "No auth token available")
            return False
        
        headers = self.get_auth_headers()
        
        # Test get agents
        try:
            response = requests.get(f"{self.api_base}/agents/", headers=headers)
            if response.status_code == 200:
                self.log_test("Get Agents", "PASS", response.status_code, "Agents retrieved")
            else:
                self.log_test("Get Agents", "FAIL", response.status_code, response.text)
        except Exception as e:
            self.log_test("Get Agents", "FAIL", None, str(e))
        
        # Test agent creation
        agent_data = {
            "name": "Test Agent",
            "type": "codegen",
            "description": "A test AI agent",
            "capabilities": ["code_generation", "testing"]
        }
        
        try:
            response = requests.post(f"{self.api_base}/agents/", json=agent_data, headers=headers)
            if response.status_code == 201:
                agent = response.json()
                self.test_agent_id = agent.get("id")
                self.log_test("Agent Creation", "PASS", response.status_code, f"Agent ID: {self.test_agent_id}")
            else:
                self.log_test("Agent Creation", "FAIL", response.status_code, response.text)
        except Exception as e:
            self.log_test("Agent Creation", "FAIL", None, str(e))
        
        return True
    
    def test_dashboard_endpoints(self):
        """Test dashboard endpoints"""
        print("\n📊 Testing Dashboard Endpoints")
        
        if not self.access_token:
            self.log_test("Dashboard Endpoints", "SKIP", None, "No auth token available")
            return False
        
        headers = self.get_auth_headers()
        
        # Test dashboard stats
        try:
            response = requests.get(f"{self.api_base}/dashboard/stats", headers=headers)
            if response.status_code == 200:
                self.log_test("Dashboard Stats", "PASS", response.status_code, "Stats retrieved")
            else:
                self.log_test("Dashboard Stats", "FAIL", response.status_code, response.text)
        except Exception as e:
            self.log_test("Dashboard Stats", "FAIL", None, str(e))
        
        # Test dashboard metrics
        try:
            response = requests.get(f"{self.api_base}/dashboard/metrics", headers=headers)
            if response.status_code == 200:
                self.log_test("Dashboard Metrics", "PASS", response.status_code, "Metrics retrieved")
            else:
                self.log_test("Dashboard Metrics", "FAIL", response.status_code, response.text)
        except Exception as e:
            self.log_test("Dashboard Metrics", "FAIL", None, str(e))
        
        return True
    
    def test_integration_endpoints(self):
        """Test integration endpoints"""
        print("\n🔗 Testing Integration Endpoints")
        
        if not self.access_token or not self.test_project_id:
            self.log_test("Integration Endpoints", "SKIP", None, "No auth token or project ID available")
            return False
        
        headers = self.get_auth_headers()
        
        # Test get integrations
        try:
            response = requests.get(f"{self.api_base}/integrations/", headers=headers)
            if response.status_code == 200:
                self.log_test("Get Integrations", "PASS", response.status_code, "Integrations retrieved")
            else:
                self.log_test("Get Integrations", "FAIL", response.status_code, response.text)
        except Exception as e:
            self.log_test("Get Integrations", "FAIL", None, str(e))
        
        # Test deployment endpoints
        try:
            response = requests.get(f"{self.api_base}/integrations/deployments", headers=headers)
            if response.status_code == 200:
                self.log_test("Get Deployments", "PASS", response.status_code, "Deployments retrieved")
            else:
                self.log_test("Get Deployments", "FAIL", response.status_code, response.text)
        except Exception as e:
            self.log_test("Get Deployments", "FAIL", None, str(e))
        
        return True
    
    def run_all_tests(self):
        """Run comprehensive tests on all endpoints"""
        print("🚀 Starting Comprehensive API Endpoint Testing")
        print("=" * 60)
        
        # Wait for server to be ready
        print("⏳ Waiting for server to be ready...")
        time.sleep(3)
        
        test_results = {
            "health": self.test_health_endpoint(),
            "auth": self.test_auth_endpoints(),
            "projects": self.test_project_endpoints(),
            "requirements": self.test_requirement_endpoints(),
            "tasks": self.test_task_endpoints(),
            "agents": self.test_agent_endpoints(),
            "dashboard": self.test_dashboard_endpoints(),
            "integrations": self.test_integration_endpoints()
        }
        
        # Summary
        print("\n" + "=" * 60)
        print("📋 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in test_results.values() if result)
        total = len(test_results)
        
        for endpoint, result in test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{endpoint.upper():12} - {status}")
        
        print(f"\nOverall Result: {passed}/{total} endpoint groups passed")
        
        if passed == total:
            print("🎉 All endpoint tests completed successfully!")
        else:
            print("⚠️  Some endpoints failed. Check the detailed logs above.")
        
        return test_results

if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()
