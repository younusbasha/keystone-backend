"""
Pytest-based API Test Suite for TechSophy Keystone
Simple and focused tests for all endpoints
"""

import pytest
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"

class TestKeystoneAPI:
    """Test class for Keystone API endpoints"""

    @pytest.fixture(scope="class")
    def auth_token(self):
        """Get authentication token for tests"""
        # Register user
        user_data = {
            "email": "pytest.user@mailinator.com",
            "username": "pytest_user",
            "first_name": "PyTest",
            "last_name": "User",
            "password": "TestPassword123"
        }

        # Try to register (might fail if user exists)
        requests.post(f"{BASE_URL}/auth/register", json=user_data)

        # Login
        login_data = {
            "username": "pytest_user",
            "password": "TestPassword123"
        }

        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        assert response.status_code == 200
        return response.json()["access_token"]

    def get_headers(self, token: str) -> Dict[str, str]:
        """Get headers with authentication"""
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Authentication Tests
    def test_register_user(self):
        """Test user registration"""
        user_data = {
            "email": "newuser@mailinator.com",
            "username": "new_test_user",
            "first_name": "New",
            "last_name": "User",
            "password": "NewPassword123"
        }

        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        assert response.status_code in [201, 400]  # 400 if user already exists

    def test_login_user(self, auth_token):
        """Test user login"""
        assert auth_token is not None

    def test_get_current_user(self, auth_token):
        """Test get current user endpoint"""
        headers = self.get_headers(auth_token)
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        assert response.status_code == 200
        assert "email" in response.json()

    # Project Tests
    def test_create_project(self, auth_token):
        """Test project creation"""
        headers = self.get_headers(auth_token)
        project_data = {
            "name": "PyTest Project",
            "description": "Test project created by pytest",
            "status": "planning",
            "priority": "medium"
        }

        response = requests.post(f"{BASE_URL}/projects/", json=project_data, headers=headers)
        assert response.status_code == 201
        assert "id" in response.json()
        return response.json()["id"]

    def test_get_projects(self, auth_token):
        """Test get projects endpoint"""
        headers = self.get_headers(auth_token)
        response = requests.get(f"{BASE_URL}/projects/", headers=headers)
        assert response.status_code == 200
        assert "projects" in response.json() or isinstance(response.json(), list)

    # Requirements Tests
    def test_create_requirement(self, auth_token):
        """Test requirement creation"""
        headers = self.get_headers(auth_token)
        # First create a project
        project_id = self.test_create_project(auth_token)

        requirement_data = {
            "title": "PyTest Requirement",
            "description": "Test requirement created by pytest",
            "project_id": project_id,
            "priority": "high",
            "status": "draft"
        }

        response = requests.post(f"{BASE_URL}/requirements/", json=requirement_data, headers=headers)
        assert response.status_code == 201

    def test_get_requirements(self, auth_token):
        """Test get requirements endpoint"""
        headers = self.get_headers(auth_token)
        response = requests.get(f"{BASE_URL}/requirements/", headers=headers)
        assert response.status_code == 200

    # Task Tests
    def test_create_task(self, auth_token):
        """Test task creation"""
        headers = self.get_headers(auth_token)
        task_data = {
            "title": "PyTest Task",
            "description": "Test task created by pytest",
            "priority": "medium",
            "status": "todo",
            "estimated_hours": 8
        }

        response = requests.post(f"{BASE_URL}/tasks/", json=task_data, headers=headers)
        assert response.status_code == 201

    def test_get_tasks(self, auth_token):
        """Test get tasks endpoint"""
        headers = self.get_headers(auth_token)
        response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
        assert response.status_code == 200

    # Dashboard Tests
    def test_dashboard_overview(self, auth_token):
        """Test dashboard overview endpoint"""
        headers = self.get_headers(auth_token)
        response = requests.get(f"{BASE_URL}/dashboard/overview", headers=headers)
        assert response.status_code == 200

    def test_dashboard_stats(self, auth_token):
        """Test dashboard stats endpoint"""
        headers = self.get_headers(auth_token)
        response = requests.get(f"{BASE_URL}/dashboard/stats", headers=headers)
        assert response.status_code == 200

    # Search Tests
    def test_global_search(self, auth_token):
        """Test global search endpoint"""
        headers = self.get_headers(auth_token)
        response = requests.get(f"{BASE_URL}/search/?q=test", headers=headers)
        assert response.status_code == 200

    # Admin Tests
    def test_system_health(self, auth_token):
        """Test system health endpoint"""
        headers = self.get_headers(auth_token)
        response = requests.get(f"{BASE_URL}/admin/health", headers=headers)
        assert response.status_code == 200

    def test_system_version(self, auth_token):
        """Test system version endpoint"""
        headers = self.get_headers(auth_token)
        response = requests.get(f"{BASE_URL}/admin/version", headers=headers)
        assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
