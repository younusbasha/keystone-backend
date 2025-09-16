"""
Comprehensive API Test Suite for TechSophy Keystone
Tests all implemented endpoints with proper authentication and data validation
"""

import asyncio
import aiohttp
import json
import pytest
import sys
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

class KeystoneAPITester:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.access_token: Optional[str] = None
        self.test_data = {}
        self.test_results = {
            "passed": 0,
            "failed": 0,
            "errors": [],
            "endpoint_results": {}
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    async def make_request(self, method: str, endpoint: str, data: Any = None,
                          files: Any = None, params: Dict = None) -> Dict[str, Any]:
        """Make HTTP request and return response"""
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers() if not files else {"Authorization": f"Bearer {self.access_token}"} if self.access_token else {}

        try:
            if method.upper() == "GET":
                async with self.session.get(url, headers=headers, params=params) as response:
                    return {
                        "status": response.status,
                        "data": await response.json() if response.content_type == 'application/json' else await response.text(),
                        "headers": dict(response.headers)
                    }
            elif method.upper() == "POST":
                if files:
                    async with self.session.post(url, headers=headers, data=files) as response:
                        return {
                            "status": response.status,
                            "data": await response.json() if response.content_type == 'application/json' else await response.text(),
                            "headers": dict(response.headers)
                        }
                else:
                    async with self.session.post(url, headers=headers, json=data) as response:
                        return {
                            "status": response.status,
                            "data": await response.json() if response.content_type == 'application/json' else await response.text(),
                            "headers": dict(response.headers)
                        }
            elif method.upper() == "PUT":
                async with self.session.put(url, headers=headers, json=data) as response:
                    return {
                        "status": response.status,
                        "data": await response.json() if response.content_type == 'application/json' else await response.text(),
                        "headers": dict(response.headers)
                    }
            elif method.upper() == "DELETE":
                async with self.session.delete(url, headers=headers) as response:
                    return {
                        "status": response.status,
                        "data": await response.json() if response.content_type == 'application/json' else await response.text(),
                        "headers": dict(response.headers)
                    }
        except Exception as e:
            return {"status": 500, "data": {"error": str(e)}, "headers": {}}

    def log_test(self, endpoint: str, method: str, status: int, expected: int, data: Any = None):
        """Log test results"""
        passed = status == expected
        result = {
            "endpoint": endpoint,
            "method": method,
            "expected_status": expected,
            "actual_status": status,
            "passed": passed,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }

        self.test_results["endpoint_results"][f"{method} {endpoint}"] = result

        if passed:
            self.test_results["passed"] += 1
            print(f"✅ {method} {endpoint} - Status: {status}")
        else:
            self.test_results["failed"] += 1
            error_msg = f"❌ {method} {endpoint} - Expected: {expected}, Got: {status}"
            self.test_results["errors"].append(error_msg)
            print(error_msg)
            if data and isinstance(data, dict) and "error" in str(data):
                print(f"   Error: {data}")

    # Authentication & User Management Tests
    async def test_auth_endpoints(self):
        """Test all authentication endpoints"""
        print("\n🔐 Testing Authentication & User Management Endpoints...")

        # Register User
        # Generate unique email for testing to avoid "already registered" error
        user_data = {
            "email": f"test.user.{datetime.now().strftime('%Y%m%d%H%M%S')}@mailinator.com",
            "username": f"test_user_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "first_name": "Test",
            "last_name": "User",
            "password": "TestPassword123"
        }

        response = await self.make_request("POST", "/auth/register", user_data)
        self.log_test("/auth/register", "POST", response["status"], 201, response["data"])

        # Login User
        login_data = {
            "username": "test_user_automated",
            "password": "TestPassword123"
        }

        response = await self.make_request("POST", "/auth/login", login_data)
        self.log_test("/auth/login", "POST", response["status"], 200, response["data"])

        if response["status"] == 200 and "access_token" in response["data"]:
            self.access_token = response["data"]["access_token"]
            print(f"🔑 Access token obtained: {self.access_token[:20]}...")

        # Get Current User
        response = await self.make_request("GET", "/auth/me")
        self.log_test("/auth/me", "GET", response["status"], 200)

        if response["status"] == 200:
            self.test_data["current_user"] = response["data"]

        # Update Current User
        update_data = {
            "first_name": "Test Updated",
            "bio": "Updated bio for testing"
        }
        response = await self.make_request("PUT", "/auth/me", update_data)
        self.log_test("/auth/me", "PUT", response["status"], 200)

        # Forgot Password
        forgot_data = {"email": "test.user@mailinator.com"}
        response = await self.make_request("POST", "/auth/forgot-password", forgot_data)
        self.log_test("/auth/forgot-password", "POST", response["status"], 200)

        # Get Users
        response = await self.make_request("GET", "/users/", params={"skip": 0, "limit": 100})
        self.log_test("/users/", "GET", response["status"], 200)

    # Project Management Tests
    async def test_project_endpoints(self):
        """Test all project management endpoints"""
        print("\n📊 Testing Project Management Endpoints...")

        # Create Project
        project_data = {
            "name": "Test E-commerce Platform",
            "description": "Automated test project for comprehensive API testing",
            "status": "planning",
            "priority": "high",
            "start_date": "2024-01-15",
            "end_date": "2024-06-30"
        }

        response = await self.make_request("POST", "/projects/", project_data)
        self.log_test("/projects/", "POST", response["status"], 201)

        if response["status"] == 201:
            self.test_data["project_id"] = response["data"]["id"]

        # Get Projects
        response = await self.make_request("GET", "/projects/", params={"skip": 0, "limit": 20})
        self.log_test("/projects/", "GET", response["status"], 200)

        # Get Project by ID
        if "project_id" in self.test_data:
            response = await self.make_request("GET", f"/projects/{self.test_data['project_id']}")
            self.log_test(f"/projects/{self.test_data['project_id']}", "GET", response["status"], 200)

            # Update Project
            update_data = {
                "name": "Test E-commerce Platform Updated",
                "description": "Updated description for testing",
                "status": "active"
            }
            response = await self.make_request("PUT", f"/projects/{self.test_data['project_id']}", update_data)
            self.log_test(f"/projects/{self.test_data['project_id']}", "PUT", response["status"], 200)

            # Get Project Stats
            response = await self.make_request("GET", f"/projects/{self.test_data['project_id']}/stats")
            self.log_test(f"/projects/{self.test_data['project_id']}/stats", "GET", response["status"], 200)

            # Get Project Team
            response = await self.make_request("GET", f"/projects/{self.test_data['project_id']}/team")
            self.log_test(f"/projects/{self.test_data['project_id']}/team", "GET", response["status"], 200)

            # Get Project Timeline
            response = await self.make_request("GET", f"/projects/{self.test_data['project_id']}/timeline")
            self.log_test(f"/projects/{self.test_data['project_id']}/timeline", "GET", response["status"], 200)

    # Requirements Management Tests
    async def test_requirement_endpoints(self):
        """Test all requirements management endpoints"""
        print("\n📋 Testing Requirements Management Endpoints...")

        # Create Requirement
        requirement_data = {
            "title": "Automated Test User Authentication System",
            "description": "Implement secure user authentication with JWT tokens for automated testing",
            "project_id": self.test_data.get("project_id"),
            "priority": "high",
            "status": "draft",
            "acceptance_criteria": "Users should be able to register, login, logout securely"
        }

        response = await self.make_request("POST", "/requirements/", requirement_data)
        self.log_test("/requirements/", "POST", response["status"], 201)

        if response["status"] == 201:
            self.test_data["requirement_id"] = response["data"]["id"]

        # Get Requirements
        response = await self.make_request("GET", "/requirements/", params={"skip": 0, "limit": 100})
        self.log_test("/requirements/", "GET", response["status"], 200)

        # Get Project Requirements
        if "project_id" in self.test_data:
            response = await self.make_request("GET", f"/requirements/project/{self.test_data['project_id']}")
            self.log_test(f"/requirements/project/{self.test_data['project_id']}", "GET", response["status"], 200)

        # Get Requirement by ID
        if "requirement_id" in self.test_data:
            response = await self.make_request("GET", f"/requirements/{self.test_data['requirement_id']}")
            self.log_test(f"/requirements/{self.test_data['requirement_id']}", "GET", response["status"], 200)

            # Analyze Requirement (AI)
            response = await self.make_request("POST", f"/requirements/{self.test_data['requirement_id']}/analyze")
            self.log_test(f"/requirements/{self.test_data['requirement_id']}/analyze", "POST", response["status"], 200)

            # Generate Tasks from Requirement (AI)
            response = await self.make_request("POST", f"/requirements/{self.test_data['requirement_id']}/generate-tasks")
            self.log_test(f"/requirements/{self.test_data['requirement_id']}/generate-tasks", "POST", response["status"], 200)

    # Task Management Tests
    async def test_task_endpoints(self):
        """Test all task management endpoints"""
        print("\n✅ Testing Task Management Endpoints...")

        # Create Task
        task_data = {
            "title": "Automated Test JWT Authentication Implementation",
            "description": "Create JWT token generation and validation system for testing",
            "project_id": self.test_data.get("project_id"),
            "requirement_id": self.test_data.get("requirement_id"),
            "priority": "high",
            "status": "todo",
            "estimated_hours": 16
        }

        response = await self.make_request("POST", "/tasks/", task_data)
        self.log_test("/tasks/", "POST", response["status"], 201)

        if response["status"] == 201:
            self.test_data["task_id"] = response["data"]["id"]

        # Get Tasks
        response = await self.make_request("GET", "/tasks/", params={"skip": 0, "limit": 100})
        self.log_test("/tasks/", "GET", response["status"], 200)

        # Get Task by ID
        if "task_id" in self.test_data:
            response = await self.make_request("GET", f"/tasks/{self.test_data['task_id']}")
            self.log_test(f"/tasks/{self.test_data['task_id']}", "GET", response["status"], 200)

            # Start Task
            response = await self.make_request("POST", f"/tasks/{self.test_data['task_id']}/start")
            self.log_test(f"/tasks/{self.test_data['task_id']}/start", "POST", response["status"], 200)

            # Add Task Comment
            comment_data = {"content": "Working on automated testing implementation"}
            response = await self.make_request("POST", f"/tasks/{self.test_data['task_id']}/comments", comment_data)
            self.log_test(f"/tasks/{self.test_data['task_id']}/comments", "POST", response["status"], 201)

            # Get Task Comments
            response = await self.make_request("GET", f"/tasks/{self.test_data['task_id']}/comments")
            self.log_test(f"/tasks/{self.test_data['task_id']}/comments", "GET", response["status"], 200)

    # AI Agents Tests
    async def test_agent_endpoints(self):
        """Test all AI agent endpoints"""
        print("\n🤖 Testing AI Agents Endpoints...")

        # Create Agent
        agent_data = {
            "name": "Automated Test Code Review Agent",
            "description": "AI agent for automated code review and quality checks in testing",
            "type": "code_review",
            "config": {
                "languages": ["python", "javascript"],
                "rules": ["security", "performance", "style"]
            }
        }

        response = await self.make_request("POST", "/agents/", agent_data)
        self.log_test("/agents/", "POST", response["status"], 201)

        if response["status"] == 201:
            self.test_data["agent_id"] = response["data"]["id"]

        # Get Agents
        response = await self.make_request("GET", "/agents/", params={"skip": 0, "limit": 100})
        self.log_test("/agents/", "GET", response["status"], 200)

        # Get Agent by ID
        if "agent_id" in self.test_data:
            response = await self.make_request("GET", f"/agents/{self.test_data['agent_id']}")
            self.log_test(f"/agents/{self.test_data['agent_id']}", "GET", response["status"], 200)

        # Get Agent Analytics
        response = await self.make_request("GET", "/agents/analytics/overview")
        self.log_test("/agents/analytics/overview", "GET", response["status"], 200)

    # Dashboard & Analytics Tests
    async def test_dashboard_endpoints(self):
        """Test all dashboard and analytics endpoints"""
        print("\n📊 Testing Dashboard & Analytics Endpoints...")

        # Get Dashboard Overview
        response = await self.make_request("GET", "/dashboard/overview")
        self.log_test("/dashboard/overview", "GET", response["status"], 200)

        # Get Dashboard Stats
        response = await self.make_request("GET", "/dashboard/stats")
        self.log_test("/dashboard/stats", "GET", response["status"], 200)

        # Get Dashboard Metrics
        response = await self.make_request("GET", "/dashboard/metrics", params={"period": "7d"})
        self.log_test("/dashboard/metrics", "GET", response["status"], 200)

        # Get Activity Feed
        response = await self.make_request("GET", "/dashboard/activity-feed", params={"skip": 0, "limit": 20})
        self.log_test("/dashboard/activity-feed", "GET", response["status"], 200)

        # Get Notifications
        response = await self.make_request("GET", "/dashboard/notifications", params={"skip": 0, "limit": 50})
        self.log_test("/dashboard/notifications", "GET", response["status"], 200)

    # Search Tests
    async def test_search_endpoints(self):
        """Test all search endpoints"""
        print("\n🔍 Testing Search Endpoints...")

        # Global Search
        response = await self.make_request("GET", "/search/", params={"q": "authentication", "skip": 0, "limit": 50})
        self.log_test("/search/", "GET", response["status"], 200)

        # Search Projects
        response = await self.make_request("GET", "/search/projects", params={"q": "test", "skip": 0, "limit": 50})
        self.log_test("/search/projects", "GET", response["status"], 200)

        # Search Requirements
        response = await self.make_request("GET", "/search/requirements", params={"q": "authentication", "skip": 0, "limit": 50})
        self.log_test("/search/requirements", "GET", response["status"], 200)

        # Search Tasks
        response = await self.make_request("GET", "/search/tasks", params={"q": "JWT", "skip": 0, "limit": 50})
        self.log_test("/search/tasks", "GET", response["status"], 200)

    # Administration Tests
    async def test_admin_endpoints(self):
        """Test all administration endpoints"""
        print("\n⚙️ Testing Administration Endpoints...")

        # Get System Health
        response = await self.make_request("GET", "/admin/health")
        self.log_test("/admin/health", "GET", response["status"], 200)

        # Get System Status
        response = await self.make_request("GET", "/admin/system-status")
        self.log_test("/admin/system-status", "GET", response["status"], 200)

        # Get System Version
        response = await self.make_request("GET", "/admin/version")
        self.log_test("/admin/version", "GET", response["status"], 200)

    # Permissions & Roles Tests
    async def test_permission_endpoints(self):
        """Test all permissions and roles endpoints"""
        print("\n🔐 Testing Permissions & Roles Endpoints...")

        # Get Permissions
        response = await self.make_request("GET", "/permissions/")
        self.log_test("/permissions/", "GET", response["status"], 200)

        # Get Roles
        response = await self.make_request("GET", "/permissions/roles")
        self.log_test("/permissions/roles", "GET", response["status"], 200)

    # Reports Tests
    async def test_report_endpoints(self):
        """Test all reports endpoints"""
        print("\n📊 Testing Reports Endpoints...")

        # Get Reports
        response = await self.make_request("GET", "/reports/", params={"skip": 0, "limit": 100})
        self.log_test("/reports/", "GET", response["status"], 200)

        # Get Report Templates
        response = await self.make_request("GET", "/reports/templates")
        self.log_test("/reports/templates", "GET", response["status"], 200)

    async def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Comprehensive API Test Suite for TechSophy Keystone")
        print("=" * 80)

        try:
            # Test authentication first (required for other tests)
            await self.test_auth_endpoints()

            # Test all other endpoints
            await self.test_project_endpoints()
            await self.test_requirement_endpoints()
            await self.test_task_endpoints()
            await self.test_agent_endpoints()
            await self.test_dashboard_endpoints()
            await self.test_search_endpoints()
            await self.test_admin_endpoints()
            await self.test_permission_endpoints()
            await self.test_report_endpoints()

        except Exception as e:
            print(f"❌ Test execution error: {str(e)}")
            self.test_results["errors"].append(f"Execution error: {str(e)}")

        # Generate test report
        await self.generate_test_report()

    async def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 80)
        print("📋 TEST RESULTS SUMMARY")
        print("=" * 80)

        total_tests = self.test_results["passed"] + self.test_results["failed"]
        success_rate = (self.test_results["passed"] / total_tests * 100) if total_tests > 0 else 0

        print(f"✅ Passed: {self.test_results['passed']}")
        print(f"❌ Failed: {self.test_results['failed']}")
        print(f"🎯 Total Tests: {total_tests}")
        print(f"📊 Success Rate: {success_rate:.1f}%")

        if self.test_results["errors"]:
            print(f"\n❌ FAILED TESTS ({len(self.test_results['errors'])}):")
            for error in self.test_results["errors"]:
                print(f"   {error}")

        # Save detailed report to file
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "passed": self.test_results["passed"],
                "failed": self.test_results["failed"],
                "success_rate": success_rate,
                "timestamp": datetime.now().isoformat()
            },
            "test_data_created": self.test_data,
            "detailed_results": self.test_results["endpoint_results"],
            "errors": self.test_results["errors"]
        }

        with open("api_test_report.json", "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n📄 Detailed report saved to: api_test_report.json")
        print("=" * 80)

async def main():
    """Main test execution function"""
    async with KeystoneAPITester() as tester:
        await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
