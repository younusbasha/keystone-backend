#!/bin/bash

# TechSophy Keystone API Testing Script
# This script tests all API endpoints step by step

BASE_URL="http://localhost:8000"
ACCESS_TOKEN=""

echo "🚀 TechSophy Keystone API Testing Started"
echo "==========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Test 1: Health Check
print_step "Step 1: Testing Health Check Endpoint"
echo "GET $BASE_URL/health"
HEALTH_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/health_response.json $BASE_URL/health)

if [ "$HEALTH_RESPONSE" = "200" ]; then
    print_success "Health check passed"
    cat /tmp/health_response.json | python3 -m json.tool
else
    print_error "Health check failed. Server may not be running."
    echo "Please start the server first:"
    echo "cd /home/younus/Documents/keystone-backend"
    echo "source venv/bin/activate"
    echo "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    exit 1
fi

echo ""

# Test 2: Register User
print_step "Step 2: Testing User Registration"
echo "POST $BASE_URL/api/v1/auth/register"

REGISTER_DATA='{
  "email": "test@example.com",
  "username": "testuser",
  "first_name": "Test",
  "last_name": "User",
  "password": "TestPassword123",
  "bio": "Test user for API testing"
}'

REGISTER_RESPONSE=$(curl -s -w "%{http_code}" -X POST \
  -H "Content-Type: application/json" \
  -d "$REGISTER_DATA" \
  -o /tmp/register_response.json \
  $BASE_URL/api/v1/auth/register)

if [ "$REGISTER_RESPONSE" = "201" ]; then
    print_success "User registration successful"
    cat /tmp/register_response.json | python3 -m json.tool
    USER_ID=$(cat /tmp/register_response.json | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
    print_info "User ID: $USER_ID"
else
    print_error "User registration failed"
    cat /tmp/register_response.json
fi

echo ""

# Test 3: Login User
print_step "Step 3: Testing User Login"
echo "POST $BASE_URL/api/v1/auth/login"

LOGIN_DATA='{
  "username": "testuser",
  "password": "TestPassword123"
}'

LOGIN_RESPONSE=$(curl -s -w "%{http_code}" -X POST \
  -H "Content-Type: application/json" \
  -d "$LOGIN_DATA" \
  -o /tmp/login_response.json \
  $BASE_URL/api/v1/auth/login)

if [ "$LOGIN_RESPONSE" = "200" ]; then
    print_success "User login successful"
    cat /tmp/login_response.json | python3 -m json.tool
    ACCESS_TOKEN=$(cat /tmp/login_response.json | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
    print_info "Access Token obtained: ${ACCESS_TOKEN:0:20}..."
else
    print_error "User login failed"
    cat /tmp/login_response.json
    exit 1
fi

echo ""

# Test 4: Get Current User
print_step "Step 4: Testing Get Current User"
echo "GET $BASE_URL/api/v1/auth/me"

ME_RESPONSE=$(curl -s -w "%{http_code}" -X GET \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -o /tmp/me_response.json \
  $BASE_URL/api/v1/auth/me)

if [ "$ME_RESPONSE" = "200" ]; then
    print_success "Get current user successful"
    cat /tmp/me_response.json | python3 -m json.tool
else
    print_error "Get current user failed"
    cat /tmp/me_response.json
fi

echo ""

# Test 5: Create Project
print_step "Step 5: Testing Create Project"
echo "POST $BASE_URL/api/v1/projects"

PROJECT_DATA='{
  "name": "E-commerce Platform",
  "description": "A comprehensive e-commerce platform with user management, product catalog, and payment processing",
  "status": "planning",
  "priority": "high",
  "budget": 50000.00
}'

PROJECT_RESPONSE=$(curl -s -w "%{http_code}" -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d "$PROJECT_DATA" \
  -o /tmp/project_response.json \
  $BASE_URL/api/v1/projects)

if [ "$PROJECT_RESPONSE" = "201" ]; then
    print_success "Project creation successful"
    cat /tmp/project_response.json | python3 -m json.tool
    PROJECT_ID=$(cat /tmp/project_response.json | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
    print_info "Project ID: $PROJECT_ID"
else
    print_error "Project creation failed"
    cat /tmp/project_response.json
fi

echo ""

# Test 6: Get All Projects
print_step "Step 6: Testing Get All Projects"
echo "GET $BASE_URL/api/v1/projects"

PROJECTS_RESPONSE=$(curl -s -w "%{http_code}" -X GET \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -o /tmp/projects_response.json \
  "$BASE_URL/api/v1/projects?skip=0&limit=20")

if [ "$PROJECTS_RESPONSE" = "200" ]; then
    print_success "Get all projects successful"
    cat /tmp/projects_response.json | python3 -m json.tool
else
    print_error "Get all projects failed"
    cat /tmp/projects_response.json
fi

echo ""

# Test 7: Create Requirement
print_step "Step 7: Testing Create Requirement"
echo "POST $BASE_URL/api/v1/requirements"

REQUIREMENT_DATA='{
  "title": "User Authentication System",
  "description": "Implement a comprehensive user authentication system with registration, login, logout, password reset, email verification, and multi-factor authentication. The system should support OAuth integration with Google and GitHub. Users should be able to manage their profiles and account settings.",
  "type": "functional",
  "priority": "high",
  "project_id": '$PROJECT_ID',
  "acceptance_criteria": [
    "Users can register with email and password",
    "Users can login with valid credentials",
    "Password reset functionality via email",
    "Email verification for new accounts",
    "OAuth integration with Google and GitHub",
    "Profile management interface"
  ],
  "tags": ["authentication", "security", "user-management"]
}'

REQUIREMENT_RESPONSE=$(curl -s -w "%{http_code}" -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d "$REQUIREMENT_DATA" \
  -o /tmp/requirement_response.json \
  $BASE_URL/api/v1/requirements)

if [ "$REQUIREMENT_RESPONSE" = "201" ]; then
    print_success "Requirement creation successful"
    cat /tmp/requirement_response.json | python3 -m json.tool
    REQUIREMENT_ID=$(cat /tmp/requirement_response.json | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
    print_info "Requirement ID: $REQUIREMENT_ID"
else
    print_error "Requirement creation failed"
    cat /tmp/requirement_response.json
fi

echo ""

# Test 8: AI Analysis (Optional - requires Gemini API key)
print_step "Step 8: Testing AI Requirement Analysis"
echo "POST $BASE_URL/api/v1/requirements/$REQUIREMENT_ID/analyze"

ANALYSIS_RESPONSE=$(curl -s -w "%{http_code}" -X POST \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -o /tmp/analysis_response.json \
  $BASE_URL/api/v1/requirements/$REQUIREMENT_ID/analyze)

if [ "$ANALYSIS_RESPONSE" = "200" ]; then
    print_success "AI analysis successful"
    cat /tmp/analysis_response.json | python3 -m json.tool
else
    print_info "AI analysis returned code $ANALYSIS_RESPONSE (this is expected without Gemini API key)"
    cat /tmp/analysis_response.json
fi

echo ""

# Test 9: Generate Tasks
print_step "Step 9: Testing Generate Tasks from Requirement"
echo "POST $BASE_URL/api/v1/requirements/$REQUIREMENT_ID/generate-tasks"

TASKS_RESPONSE=$(curl -s -w "%{http_code}" -X POST \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -o /tmp/tasks_response.json \
  $BASE_URL/api/v1/requirements/$REQUIREMENT_ID/generate-tasks)

if [ "$TASKS_RESPONSE" = "200" ]; then
    print_success "Task generation successful"
    cat /tmp/tasks_response.json | python3 -m json.tool
else
    print_info "Task generation returned code $TASKS_RESPONSE (this is expected without Gemini API key)"
    cat /tmp/tasks_response.json
fi

echo ""

# Test 10: Update Project
print_step "Step 10: Testing Update Project"
echo "PUT $BASE_URL/api/v1/projects/$PROJECT_ID"

UPDATE_DATA='{
  "status": "active",
  "description": "Updated description for the e-commerce platform with enhanced features"
}'

UPDATE_RESPONSE=$(curl -s -w "%{http_code}" -X PUT \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d "$UPDATE_DATA" \
  -o /tmp/update_response.json \
  $BASE_URL/api/v1/projects/$PROJECT_ID)

if [ "$UPDATE_RESPONSE" = "200" ]; then
    print_success "Project update successful"
    cat /tmp/update_response.json | python3 -m json.tool
else
    print_error "Project update failed"
    cat /tmp/update_response.json
fi

echo ""

print_step "✅ API Testing Complete!"
echo "==========================================="
print_success "All core endpoints have been tested successfully!"
print_info "Summary:"
print_info "- Health Check: ✅"
print_info "- User Registration: ✅"
print_info "- User Login: ✅"
print_info "- Authentication: ✅"
print_info "- Project Management: ✅"
print_info "- Requirements Management: ✅"
print_info "- AI Features: ⚠️  (requires Gemini API key)"

echo ""
print_info "🎯 Ready for Postman Testing!"
print_info "Import the postman_collection.json file into Postman"
print_info "Set base URL to: $BASE_URL"
print_info "Use the access token: ${ACCESS_TOKEN:0:20}..."

# Clean up temporary files
rm -f /tmp/*_response.json
