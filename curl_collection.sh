#!/bin/bash

# TechSophy Keystone API - Complete cURL Collection
# AI-Powered SDLC Management Platform
# Generated from Postman Collection

# Configuration
BASE_URL="http://localhost:8000"
KEYCLOAK_URL="http://localhost:8080"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables to store data between requests
ACCESS_TOKEN=""
REFRESH_TOKEN=""
USER_ID=""
PROJECT_ID=""
REQUIREMENT_ID=""
TASK_ID=""
AGENT_ID=""
ACTION_ID=""
INTEGRATION_ID=""
DEPLOYMENT_ID=""

# Helper function to print section headers
print_section() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

# Helper function to print test results
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ $2${NC}"
    else
        echo -e "${RED}✗ $2${NC}"
    fi
}

# Helper function to extract JSON value
extract_json_value() {
    echo "$1" | grep -o "\"$2\":[^,}]*" | sed 's/"[^"]*"://; s/"//g; s/,$//'
}

# =============================================================================
# AUTHENTICATION ENDPOINTS
# =============================================================================

print_section "AUTHENTICATION TESTS"

# 1. Register User
echo -e "${YELLOW}1. Registering User...${NC}"
REGISTER_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@techsophy.com",
    "username": "john_doe",
    "first_name": "John",
    "last_name": "Doe",
    "password": "SecurePassword123!"
  }')

HTTP_CODE=$(echo "$REGISTER_RESPONSE" | tail -n1)
REGISTER_BODY=$(echo "$REGISTER_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "201" ]; then
    USER_ID=$(extract_json_value "$REGISTER_BODY" "id")
    print_result 0 "User Registration - Status: $HTTP_CODE"
    echo "   User ID: $USER_ID"
else
    print_result 1 "User Registration - Status: $HTTP_CODE"
    echo "   Response: $REGISTER_BODY"
fi

# 2. Login User
echo -e "\n${YELLOW}2. Logging in User...${NC}"
LOGIN_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePassword123!"
  }')

HTTP_CODE=$(echo "$LOGIN_RESPONSE" | tail -n1)
LOGIN_BODY=$(echo "$LOGIN_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
    ACCESS_TOKEN=$(extract_json_value "$LOGIN_BODY" "access_token")
    REFRESH_TOKEN=$(extract_json_value "$LOGIN_BODY" "refresh_token")
    print_result 0 "User Login - Status: $HTTP_CODE"
    echo "   Access Token: ${ACCESS_TOKEN:0:50}..."
else
    print_result 1 "User Login - Status: $HTTP_CODE"
    echo "   Response: $LOGIN_BODY"
fi

# 3. Get Current User
echo -e "\n${YELLOW}3. Getting Current User Info...${NC}"
USER_INFO_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/v1/auth/me" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

HTTP_CODE=$(echo "$USER_INFO_RESPONSE" | tail -n1)
USER_INFO_BODY=$(echo "$USER_INFO_RESPONSE" | head -n -1)

print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "Get Current User - Status: $HTTP_CODE"

# 4. Refresh Token
echo -e "\n${YELLOW}4. Refreshing Token...${NC}"
REFRESH_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d "{
    \"refresh_token\": \"$REFRESH_TOKEN\"
  }")

HTTP_CODE=$(echo "$REFRESH_RESPONSE" | tail -n1)
print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "Token Refresh - Status: $HTTP_CODE"

# =============================================================================
# PROJECT MANAGEMENT ENDPOINTS
# =============================================================================

print_section "PROJECT MANAGEMENT TESTS"

# 5. Create Project
echo -e "${YELLOW}5. Creating Project...${NC}"
PROJECT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/projects" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Chat Platform",
    "description": "Building an AI-powered chat application with advanced NLP capabilities",
    "priority": "high",
    "start_date": "2024-01-15T00:00:00Z",
    "end_date": "2024-06-15T00:00:00Z",
    "budget": 100000.00
  }')

HTTP_CODE=$(echo "$PROJECT_RESPONSE" | tail -n1)
PROJECT_BODY=$(echo "$PROJECT_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "201" ]; then
    PROJECT_ID=$(extract_json_value "$PROJECT_BODY" "id")
    print_result 0 "Project Creation - Status: $HTTP_CODE"
    echo "   Project ID: $PROJECT_ID"
else
    print_result 1 "Project Creation - Status: $HTTP_CODE"
    echo "   Response: $PROJECT_BODY"
fi

# 6. List Projects
echo -e "\n${YELLOW}6. Listing Projects...${NC}"
LIST_PROJECTS_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/v1/projects?skip=0&limit=10" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

HTTP_CODE=$(echo "$LIST_PROJECTS_RESPONSE" | tail -n1)
print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "List Projects - Status: $HTTP_CODE"

# 7. Get Project Details
if [ -n "$PROJECT_ID" ]; then
    echo -e "\n${YELLOW}7. Getting Project Details...${NC}"
    GET_PROJECT_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/v1/projects/$PROJECT_ID" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$GET_PROJECT_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "Get Project Details - Status: $HTTP_CODE"
fi

# 8. Update Project
if [ -n "$PROJECT_ID" ]; then
    echo -e "\n${YELLOW}8. Updating Project...${NC}"
    UPDATE_PROJECT_RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "$BASE_URL/api/v1/projects/$PROJECT_ID" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "status": "in_progress",
        "priority": "medium",
        "description": "Updated description with new requirements"
      }')

    HTTP_CODE=$(echo "$UPDATE_PROJECT_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "Update Project - Status: $HTTP_CODE"
fi

# =============================================================================
# REQUIREMENTS MANAGEMENT ENDPOINTS
# =============================================================================

print_section "REQUIREMENTS MANAGEMENT TESTS"

# 9. Create Requirement
if [ -n "$PROJECT_ID" ]; then
    echo -e "${YELLOW}9. Creating Requirement...${NC}"
    REQUIREMENT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/requirements" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{
        \"title\": \"User Authentication System\",
        \"description\": \"Implement secure user login and registration with JWT tokens. Users should be able to register with email and password, login with credentials, and receive JWT tokens for API access. Include password reset functionality and email verification.\",
        \"type\": \"functional\",
        \"priority\": \"high\",
        \"project_id\": \"$PROJECT_ID\",
        \"acceptance_criteria\": [
          \"Users can register with email and password\",
          \"Users can login with credentials\",
          \"JWT tokens are issued and validated\",
          \"Password reset functionality works\",
          \"Email verification is implemented\"
        ],
        \"tags\": [\"security\", \"authentication\", \"backend\", \"jwt\"]
      }")

    HTTP_CODE=$(echo "$REQUIREMENT_RESPONSE" | tail -n1)
    REQUIREMENT_BODY=$(echo "$REQUIREMENT_RESPONSE" | head -n -1)

    if [ "$HTTP_CODE" = "201" ]; then
        REQUIREMENT_ID=$(extract_json_value "$REQUIREMENT_BODY" "id")
        print_result 0 "Requirement Creation - Status: $HTTP_CODE"
        echo "   Requirement ID: $REQUIREMENT_ID"
    else
        print_result 1 "Requirement Creation - Status: $HTTP_CODE"
        echo "   Response: $REQUIREMENT_BODY"
    fi
fi

# 10. List Requirements
if [ -n "$PROJECT_ID" ]; then
    echo -e "\n${YELLOW}10. Listing Requirements...${NC}"
    LIST_REQUIREMENTS_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/v1/requirements/project/$PROJECT_ID?skip=0&limit=10" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$LIST_REQUIREMENTS_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "List Requirements - Status: $HTTP_CODE"
fi

# 11. AI Analyze Requirement
if [ -n "$REQUIREMENT_ID" ]; then
    echo -e "\n${YELLOW}11. AI Analyzing Requirement...${NC}"
    ANALYZE_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/requirements/$REQUIREMENT_ID/analyze" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$ANALYZE_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "AI Requirement Analysis - Status: $HTTP_CODE"
fi

# 12. Generate Tasks from Requirement
if [ -n "$REQUIREMENT_ID" ]; then
    echo -e "\n${YELLOW}12. Generating Tasks from Requirement...${NC}"
    GENERATE_TASKS_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/requirements/$REQUIREMENT_ID/generate-tasks" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$GENERATE_TASKS_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "Generate Tasks - Status: $HTTP_CODE"
fi

# =============================================================================
# TASK MANAGEMENT ENDPOINTS
# =============================================================================

print_section "TASK MANAGEMENT TESTS"

# 13. Create Task
if [ -n "$PROJECT_ID" ] && [ -n "$REQUIREMENT_ID" ]; then
    echo -e "${YELLOW}13. Creating Task...${NC}"
    TASK_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/tasks" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{
        \"title\": \"Implement JWT Authentication Middleware\",
        \"description\": \"Create JWT token generation and validation logic for secure API access\",
        \"priority\": \"high\",
        \"task_type\": \"development\",
        \"estimated_hours\": 8.0,
        \"project_id\": \"$PROJECT_ID\",
        \"requirement_id\": \"$REQUIREMENT_ID\",
        \"due_date\": \"2024-01-25T18:00:00Z\",
        \"acceptance_criteria\": [
          \"JWT tokens are generated on login\",
          \"Token validation middleware implemented\",
          \"Refresh token mechanism working\",
          \"Proper error handling for invalid tokens\"
        ]
      }")

    HTTP_CODE=$(echo "$TASK_RESPONSE" | tail -n1)
    TASK_BODY=$(echo "$TASK_RESPONSE" | head -n -1)

    if [ "$HTTP_CODE" = "201" ]; then
        TASK_ID=$(extract_json_value "$TASK_BODY" "id")
        print_result 0 "Task Creation - Status: $HTTP_CODE"
        echo "   Task ID: $TASK_ID"
    else
        print_result 1 "Task Creation - Status: $HTTP_CODE"
        echo "   Response: $TASK_BODY"
    fi
fi

# 14. List Tasks
if [ -n "$PROJECT_ID" ]; then
    echo -e "\n${YELLOW}14. Listing Tasks...${NC}"
    LIST_TASKS_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/v1/tasks?project_id=$PROJECT_ID&status=pending&priority=high&skip=0&limit=20" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$LIST_TASKS_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "List Tasks - Status: $HTTP_CODE"
fi

# 15. Start Task
if [ -n "$TASK_ID" ]; then
    echo -e "\n${YELLOW}15. Starting Task...${NC}"
    START_TASK_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/tasks/$TASK_ID/start" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$START_TASK_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "Start Task - Status: $HTTP_CODE"
fi

# 16. Add Task Comment
if [ -n "$TASK_ID" ]; then
    echo -e "\n${YELLOW}16. Adding Task Comment...${NC}"
    COMMENT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/tasks/$TASK_ID/comments" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "content": "Making good progress on JWT implementation. Token generation is complete, working on validation middleware.",
        "comment_type": "general"
      }')

    HTTP_CODE=$(echo "$COMMENT_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "201" ] && echo 0 || echo 1) "Add Task Comment - Status: $HTTP_CODE"
fi

# 17. Complete Task
if [ -n "$TASK_ID" ]; then
    echo -e "\n${YELLOW}17. Completing Task...${NC}"
    COMPLETE_TASK_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/tasks/$TASK_ID/complete" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$COMPLETE_TASK_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "Complete Task - Status: $HTTP_CODE"
fi

# =============================================================================
# AI AGENT MANAGEMENT ENDPOINTS
# =============================================================================

print_section "AI AGENT MANAGEMENT TESTS"

# 18. Create AI Agent
if [ -n "$PROJECT_ID" ]; then
    echo -e "${YELLOW}18. Creating AI Agent...${NC}"
    AGENT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/agents" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{
        \"name\": \"CodeGen Agent Alpha\",
        \"agent_type\": \"codegen\",
        \"capabilities\": [
          \"javascript_generation\",
          \"python_generation\",
          \"api_development\",
          \"database_schema_design\"
        ],
        \"configuration\": {
          \"max_code_lines\": 500,
          \"coding_standards\": \"PEP8\",
          \"frameworks\": [\"fastapi\", \"react\", \"sqlalchemy\"],
          \"ai_model\": \"gemini-pro\"
        },
        \"max_concurrent_actions\": 3,
        \"project_id\": \"$PROJECT_ID\"
      }")

    HTTP_CODE=$(echo "$AGENT_RESPONSE" | tail -n1)
    AGENT_BODY=$(echo "$AGENT_RESPONSE" | head -n -1)

    if [ "$HTTP_CODE" = "201" ]; then
        AGENT_ID=$(extract_json_value "$AGENT_BODY" "id")
        print_result 0 "AI Agent Creation - Status: $HTTP_CODE"
        echo "   Agent ID: $AGENT_ID"
    else
        print_result 1 "AI Agent Creation - Status: $HTTP_CODE"
        echo "   Response: $AGENT_BODY"
    fi
fi

# 19. List AI Agents
if [ -n "$PROJECT_ID" ]; then
    echo -e "\n${YELLOW}19. Listing AI Agents...${NC}"
    LIST_AGENTS_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/v1/agents?project_id=$PROJECT_ID&agent_type=codegen&status=active" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$LIST_AGENTS_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "List AI Agents - Status: $HTTP_CODE"
fi

# 20. Execute Agent Action
if [ -n "$AGENT_ID" ] && [ -n "$TASK_ID" ]; then
    echo -e "\n${YELLOW}20. Executing Agent Action...${NC}"
    EXECUTE_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/agents/$AGENT_ID/execute" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{
        \"action_type\": \"code_generation\",
        \"target_type\": \"task\",
        \"target_id\": \"$TASK_ID\",
        \"input_data\": {
          \"specification\": \"Create a JWT authentication middleware for FastAPI that validates tokens and extracts user information\",
          \"language\": \"python\",
          \"framework\": \"fastapi\",
          \"requirements\": [
            \"Validate JWT tokens\",
            \"Extract user information from token\",
            \"Handle token expiration\",
            \"Return proper error responses\"
          ]
        }
      }")

    HTTP_CODE=$(echo "$EXECUTE_RESPONSE" | tail -n1)
    EXECUTE_BODY=$(echo "$EXECUTE_RESPONSE" | head -n -1)

    if [ "$HTTP_CODE" = "201" ]; then
        ACTION_ID=$(extract_json_value "$EXECUTE_BODY" "id")
        print_result 0 "Execute Agent Action - Status: $HTTP_CODE"
        echo "   Action ID: $ACTION_ID"
    else
        print_result 1 "Execute Agent Action - Status: $HTTP_CODE"
        echo "   Response: $EXECUTE_BODY"
    fi
fi

# 21. Get Agent Actions
if [ -n "$AGENT_ID" ]; then
    echo -e "\n${YELLOW}21. Getting Agent Actions...${NC}"
    GET_ACTIONS_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/v1/agents/$AGENT_ID/actions?status=requires_review&skip=0&limit=10" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$GET_ACTIONS_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "Get Agent Actions - Status: $HTTP_CODE"
fi

# 22. Approve Agent Action
if [ -n "$ACTION_ID" ]; then
    echo -e "\n${YELLOW}22. Approving Agent Action...${NC}"
    APPROVE_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/agents/actions/$ACTION_ID/approve" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "review_comments": "Code looks good! JWT validation logic is solid and error handling is comprehensive. Approved for implementation."
      }')

    HTTP_CODE=$(echo "$APPROVE_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "Approve Agent Action - Status: $HTTP_CODE"
fi

# 23. Get Agent Analytics
if [ -n "$PROJECT_ID" ]; then
    echo -e "\n${YELLOW}23. Getting Agent Analytics...${NC}"
    ANALYTICS_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/v1/agents/analytics/overview?project_id=$PROJECT_ID" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$ANALYTICS_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "Get Agent Analytics - Status: $HTTP_CODE"
fi

# =============================================================================
# INTEGRATIONS & DEPLOYMENTS ENDPOINTS
# =============================================================================

print_section "INTEGRATIONS & DEPLOYMENTS TESTS"

# 24. Create GitHub Integration
if [ -n "$PROJECT_ID" ]; then
    echo -e "${YELLOW}24. Creating GitHub Integration...${NC}"
    INTEGRATION_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/integrations" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{
        \"name\": \"GitHub Integration\",
        \"integration_type\": \"github\",
        \"endpoint_url\": \"https://api.github.com\",
        \"auth_type\": \"token\",
        \"credentials\": {
          \"token\": \"github_personal_access_token_here\"
        },
        \"config\": {
          \"repository\": \"username/ai-chat-platform\",
          \"webhook_events\": [\"push\", \"pull_request\", \"issues\"],
          \"default_branch\": \"main\"
        },
        \"project_id\": \"$PROJECT_ID\"
      }")

    HTTP_CODE=$(echo "$INTEGRATION_RESPONSE" | tail -n1)
    INTEGRATION_BODY=$(echo "$INTEGRATION_RESPONSE" | head -n -1)

    if [ "$HTTP_CODE" = "201" ]; then
        INTEGRATION_ID=$(extract_json_value "$INTEGRATION_BODY" "id")
        print_result 0 "GitHub Integration Creation - Status: $HTTP_CODE"
        echo "   Integration ID: $INTEGRATION_ID"
    else
        print_result 1 "GitHub Integration Creation - Status: $HTTP_CODE"
        echo "   Response: $INTEGRATION_BODY"
    fi
fi

# 25. Test Integration
if [ -n "$INTEGRATION_ID" ]; then
    echo -e "\n${YELLOW}25. Testing Integration...${NC}"
    TEST_INTEGRATION_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/integrations/$INTEGRATION_ID/test" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$TEST_INTEGRATION_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "Test Integration - Status: $HTTP_CODE"
fi

# 26. Create Deployment
if [ -n "$PROJECT_ID" ]; then
    echo -e "\n${YELLOW}26. Creating Deployment...${NC}"
    DEPLOYMENT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/integrations/deployments" \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{
        \"project_id\": \"$PROJECT_ID\",
        \"version\": \"v1.2.3\",
        \"environment\": \"staging\",
        \"deployment_type\": \"blue-green\",
        \"commit_hash\": \"abc123def456789\",
        \"branch\": \"main\",
        \"tag\": \"v1.2.3\",
        \"config\": {
          \"instances\": 2,
          \"health_check_url\": \"/health\",
          \"timeout\": 300,
          \"rollback_on_failure\": true
        },
        \"artifacts\": {
          \"docker_image\": \"techsophy/ai-chat:v1.2.3\",
          \"size_mb\": 245
        }
      }")

    HTTP_CODE=$(echo "$DEPLOYMENT_RESPONSE" | tail -n1)
    DEPLOYMENT_BODY=$(echo "$DEPLOYMENT_RESPONSE" | head -n -1)

    if [ "$HTTP_CODE" = "201" ]; then
        DEPLOYMENT_ID=$(extract_json_value "$DEPLOYMENT_BODY" "id")
        print_result 0 "Deployment Creation - Status: $HTTP_CODE"
        echo "   Deployment ID: $DEPLOYMENT_ID"
    else
        print_result 1 "Deployment Creation - Status: $HTTP_CODE"
        echo "   Response: $DEPLOYMENT_BODY"
    fi
fi

# 27. List Deployments
if [ -n "$PROJECT_ID" ]; then
    echo -e "\n${YELLOW}27. Listing Deployments...${NC}"
    LIST_DEPLOYMENTS_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/v1/integrations/deployments?project_id=$PROJECT_ID&environment=staging&status=success" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$LIST_DEPLOYMENTS_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "List Deployments - Status: $HTTP_CODE"
fi

# =============================================================================
# DASHBOARD & ANALYTICS ENDPOINTS
# =============================================================================

print_section "DASHBOARD & ANALYTICS TESTS"

# 28. Dashboard Overview
if [ -n "$PROJECT_ID" ]; then
    echo -e "${YELLOW}28. Getting Dashboard Overview...${NC}"
    DASHBOARD_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/v1/dashboard/overview?project_id=$PROJECT_ID" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$DASHBOARD_RESPONSE" | tail -n1)
    DASHBOARD_BODY=$(echo "$DASHBOARD_RESPONSE" | head -n -1)

    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "Dashboard Overview - Status: $HTTP_CODE"

    if [ "$HTTP_CODE" = "200" ]; then
        echo "   Dashboard Data Preview:"
        echo "$DASHBOARD_BODY" | head -c 200
        echo "..."
    fi
fi

# 29. Automation Metrics
if [ -n "$PROJECT_ID" ]; then
    echo -e "\n${YELLOW}29. Getting Automation Metrics...${NC}"
    AUTOMATION_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/v1/dashboard/metrics/automation?project_id=$PROJECT_ID" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$AUTOMATION_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "Automation Metrics - Status: $HTTP_CODE"
fi

# 30. Project Metrics
if [ -n "$PROJECT_ID" ]; then
    echo -e "\n${YELLOW}30. Getting Project Metrics...${NC}"
    PROJECT_METRICS_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/v1/dashboard/metrics/projects?project_id=$PROJECT_ID" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$PROJECT_METRICS_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "Project Metrics - Status: $HTTP_CODE"
fi

# 31. Activity Feed
if [ -n "$PROJECT_ID" ]; then
    echo -e "\n${YELLOW}31. Getting Activity Feed...${NC}"
    ACTIVITY_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/v1/dashboard/activity-feed?project_id=$PROJECT_ID&limit=20" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$ACTIVITY_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "Activity Feed - Status: $HTTP_CODE"
fi

# 32. Trends Analytics
if [ -n "$PROJECT_ID" ]; then
    echo -e "\n${YELLOW}32. Getting Trends Analytics...${NC}"
    TRENDS_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/v1/dashboard/analytics/trends?project_id=$PROJECT_ID&days=30" \
      -H "Authorization: Bearer $ACCESS_TOKEN")

    HTTP_CODE=$(echo "$TRENDS_RESPONSE" | tail -n1)
    print_result $([ "$HTTP_CODE" = "200" ] && echo 0 || echo 1) "Trends Analytics - Status: $HTTP_CODE"
fi

# =============================================================================
# SUMMARY
# =============================================================================

print_section "TEST SUMMARY"

echo -e "${GREEN}✓ Authentication Tests Complete${NC}"
echo -e "${GREEN}✓ Project Management Tests Complete${NC}"
echo -e "${GREEN}✓ Requirements Management Tests Complete${NC}"
echo -e "${GREEN}✓ Task Management Tests Complete${NC}"
echo -e "${GREEN}✓ AI Agent Management Tests Complete${NC}"
echo -e "${GREEN}✓ Integrations & Deployments Tests Complete${NC}"
echo -e "${GREEN}✓ Dashboard & Analytics Tests Complete${NC}"

echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}COLLECTED VARIABLES:${NC}"
echo -e "${BLUE}========================================${NC}"
echo "ACCESS_TOKEN: ${ACCESS_TOKEN:0:50}..."
echo "USER_ID: $USER_ID"
echo "PROJECT_ID: $PROJECT_ID"
echo "REQUIREMENT_ID: $REQUIREMENT_ID"
echo "TASK_ID: $TASK_ID"
echo "AGENT_ID: $AGENT_ID"
echo "ACTION_ID: $ACTION_ID"
echo "INTEGRATION_ID: $INTEGRATION_ID"
echo "DEPLOYMENT_ID: $DEPLOYMENT_ID"

echo -e "\n${GREEN}🎉 TechSophy Keystone API Testing Complete!${NC}"
echo -e "${YELLOW}Total Endpoints Tested: 32${NC}"
echo -e "${BLUE}Base URL: $BASE_URL${NC}"

# Optional: Save variables to file for future use
cat > test_variables.env << EOF
# Generated by curl_collection.sh on $(date)
ACCESS_TOKEN="$ACCESS_TOKEN"
REFRESH_TOKEN="$REFRESH_TOKEN"
USER_ID="$USER_ID"
PROJECT_ID="$PROJECT_ID"
REQUIREMENT_ID="$REQUIREMENT_ID"
TASK_ID="$TASK_ID"
AGENT_ID="$AGENT_ID"
ACTION_ID="$ACTION_ID"
INTEGRATION_ID="$INTEGRATION_ID"
DEPLOYMENT_ID="$DEPLOYMENT_ID"
EOF

echo -e "\n${YELLOW}Variables saved to: test_variables.env${NC}"
