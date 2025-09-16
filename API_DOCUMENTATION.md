# TechSophy Keystone API Documentation

## 🚀 AI-Powered SDLC Management Platform

TechSophy Keystone is a comprehensive Software Development Lifecycle (SDLC) Management Platform that leverages AI to automate and streamline the entire software development process.

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [User Roles & Personas](#user-roles--personas)
- [Core Workflows](#core-workflows)
- [Authentication](#authentication)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

## ✨ Features

### Core Functionality
- **User Authentication & Authorization**: JWT-based secure authentication system
- **Project Management**: Complete CRUD operations for project lifecycle management
- **Requirements Management**: Advanced requirements tracking with AI analysis
- **AI-Powered Task Generation**: Automatic task breakdown from requirements
- **AI Agent Management**: Autonomous task execution with human oversight
- **Integration Management**: External service integrations (GitHub, Jira, Jenkins, etc.)
- **Deployment Automation**: Automated deployment with health monitoring
- **Real-time Dashboard**: Comprehensive analytics and metrics
- **Audit & Compliance**: Complete activity tracking and security monitoring

### AI-Powered Features
- **80%+ Task Automation**: AI agents handle routine development work
- **Intelligent Requirement Analysis**: NLP processing with confidence scoring
- **Autonomous Decision Making**: AI agents make decisions within defined parameters
- **Human-in-the-loop Validation**: Risk escalation and approval workflows
- **Predictive Analytics**: Project risk assessment and performance metrics

## 🛠 Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with async SQLAlchemy
- **Caching**: Redis
- **AI Integration**: Google Gemini AI
- **Authentication**: JWT tokens with refresh mechanism
- **Containerization**: Docker & Docker Compose
- **API Documentation**: OpenAPI/Swagger

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Google AI API Key

### Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd keystone-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://user:password@localhost/keystone_db"
export REDIS_URL="redis://localhost:6379"
export GOOGLE_AI_API_KEY="your_gemini_api_key"
export SECRET_KEY="your_secret_key"
```

### Run the Application
```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Using Docker
docker-compose up -d
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- ReDoc Documentation: `http://localhost:8000/redoc`

## 🔐 Authentication

All endpoints (except registration and login) require JWT authentication.

### Authentication Flow
1. **Register**: `POST /api/v1/auth/register`
2. **Login**: `POST /api/v1/auth/login` - Returns access and refresh tokens
3. **Use Token**: Include in header: `Authorization: Bearer <access_token>`
4. **Refresh**: `POST /api/v1/auth/refresh` - Get new access token

### Token Expiry
- **Access Token**: 30 minutes
- **Refresh Token**: 7 days

## 👥 User Roles & Personas

### 1. Project Manager (PM)
**Responsibilities**: Project oversight, team productivity monitoring, AI agent performance management
**Key Permissions**: 
- Full project access
- Team member management
- Agent configuration
- Dashboard analytics

### 2. Business Analyst (BA)
**Responsibilities**: Requirements input, collaboration with AI agents, business needs translation
**Key Permissions**:
- Requirements management
- AI analysis triggering
- Epic generation
- Stakeholder communication

### 3. Developer
**Responsibilities**: Task execution, code review, technical implementation
**Key Permissions**:
- Task access and updates
- Code repository integration
- AI-generated code review
- Technical documentation

### 4. Reviewer
**Responsibilities**: Quality assurance, agent activity review, approval workflows
**Key Permissions**:
- Agent action review
- Code quality assessment
- Approval/rejection workflows
- Audit trail access

## 📡 API Endpoints

### Authentication Endpoints

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "john_doe",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securePassword123"
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securePassword123"
}
```

#### Get Current User
```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

#### Refresh Token
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "<refresh_token>"
}
```

### Project Management Endpoints

#### Create Project
```http
POST /api/v1/projects
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "AI Chat Platform",
  "description": "Building an AI-powered chat application",
  "priority": "high",
  "start_date": "2024-01-15T00:00:00Z",
  "end_date": "2024-06-15T00:00:00Z",
  "budget": 100000.00
}
```

#### List Projects
```http
GET /api/v1/projects?skip=0&limit=10&status=active
Authorization: Bearer <access_token>
```

#### Get Project
```http
GET /api/v1/projects/{project_id}
Authorization: Bearer <access_token>
```

#### Update Project
```http
PUT /api/v1/projects/{project_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Updated Project Name",
  "status": "in_progress",
  "priority": "medium"
}
```

#### Delete Project
```http
DELETE /api/v1/projects/{project_id}
Authorization: Bearer <access_token>
```

### Requirements Management Endpoints

#### Create Requirement
```http
POST /api/v1/requirements
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "User Authentication System",
  "description": "Implement secure user login and registration with JWT tokens",
  "type": "functional",
  "priority": "high",
  "project_id": "project_uuid",
  "acceptance_criteria": [
    "Users can register with email and password",
    "Users can login with credentials",
    "JWT tokens are issued and validated"
  ],
  "tags": ["security", "authentication", "backend"]
}
```

#### List Requirements
```http
GET /api/v1/requirements/project/{project_id}?skip=0&limit=10
Authorization: Bearer <access_token>
```

#### Get Requirement
```http
GET /api/v1/requirements/{requirement_id}
Authorization: Bearer <access_token>
```

#### AI Requirement Analysis
```http
POST /api/v1/requirements/{requirement_id}/analyze
Authorization: Bearer <access_token>
```

#### Generate Tasks from Requirement
```http
POST /api/v1/requirements/{requirement_id}/generate-tasks
Authorization: Bearer <access_token>
```

### Task Management Endpoints

#### Create Task
```http
POST /api/v1/tasks
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Implement JWT Authentication",
  "description": "Create JWT token generation and validation logic",
  "priority": "high",
  "task_type": "development",
  "estimated_hours": 8.0,
  "project_id": "project_uuid",
  "requirement_id": "requirement_uuid",
  "due_date": "2024-01-20T18:00:00Z",
  "acceptance_criteria": [
    "JWT tokens are generated on login",
    "Token validation middleware implemented",
    "Refresh token mechanism working"
  ]
}
```

#### List Tasks
```http
GET /api/v1/tasks?project_id=uuid&status=pending&priority=high&skip=0&limit=20
Authorization: Bearer <access_token>
```

#### Get Task
```http
GET /api/v1/tasks/{task_id}
Authorization: Bearer <access_token>
```

#### Update Task
```http
PUT /api/v1/tasks/{task_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "in_progress",
  "actual_hours": 3.5
}
```

#### Assign Task
```http
POST /api/v1/tasks/{task_id}/assign/{user_id}
Authorization: Bearer <access_token>
```

#### Start Task
```http
POST /api/v1/tasks/{task_id}/start
Authorization: Bearer <access_token>
```

#### Complete Task
```http
POST /api/v1/tasks/{task_id}/complete
Authorization: Bearer <access_token>
```

#### Add Task Comment
```http
POST /api/v1/tasks/{task_id}/comments
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "content": "Making good progress on JWT implementation",
  "comment_type": "general"
}
```

#### Add Task Dependency
```http
POST /api/v1/tasks/{task_id}/dependencies
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "depends_on_id": "prerequisite_task_uuid",
  "dependency_type": "blocks"
}
```

### AI Agent Management Endpoints

#### Create AI Agent
```http
POST /api/v1/agents
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "CodeGen Agent Alpha",
  "agent_type": "codegen",
  "capabilities": [
    "javascript_generation",
    "python_generation",
    "api_development"
  ],
  "configuration": {
    "max_code_lines": 500,
    "coding_standards": "PEP8",
    "frameworks": ["fastapi", "react"]
  },
  "max_concurrent_actions": 3,
  "project_id": "project_uuid"
}
```

#### List AI Agents
```http
GET /api/v1/agents?project_id=uuid&agent_type=codegen&status=active
Authorization: Bearer <access_token>
```

#### Execute Agent Action
```http
POST /api/v1/agents/{agent_id}/execute
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "action_type": "code_generation",
  "target_type": "task",
  "target_id": "task_uuid",
  "input_data": {
    "specification": "Create a JWT authentication middleware",
    "language": "python",
    "framework": "fastapi"
  }
}
```

#### Get Agent Actions
```http
GET /api/v1/agents/{agent_id}/actions?status=requires_review&skip=0&limit=10
Authorization: Bearer <access_token>
```

#### Approve Agent Action
```http
POST /api/v1/agents/actions/{action_id}/approve
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "review_comments": "Code looks good, approved for implementation"
}
```

#### Reject Agent Action
```http
POST /api/v1/agents/actions/{action_id}/reject
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "review_comments": "Code needs refactoring for better error handling"
}
```

#### Get Agent Analytics
```http
GET /api/v1/agents/analytics/overview?project_id=uuid
Authorization: Bearer <access_token>
```

### Integration & Deployment Endpoints

#### Create Integration
```http
POST /api/v1/integrations
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "GitHub Integration",
  "integration_type": "github",
  "endpoint_url": "https://api.github.com",
  "auth_type": "token",
  "credentials": {
    "token": "github_personal_access_token"
  },
  "config": {
    "repository": "username/repository",
    "webhook_events": ["push", "pull_request"]
  },
  "project_id": "project_uuid"
}
```

#### List Integrations
```http
GET /api/v1/integrations?project_id=uuid&integration_type=github&status=active
Authorization: Bearer <access_token>
```

#### Test Integration
```http
POST /api/v1/integrations/{integration_id}/test
Authorization: Bearer <access_token>
```

#### Create Deployment
```http
POST /api/v1/integrations/deployments
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "project_id": "project_uuid",
  "version": "v1.2.3",
  "environment": "production",
  "deployment_type": "blue-green",
  "commit_hash": "abc123def456",
  "branch": "main",
  "config": {
    "instances": 3,
    "health_check_url": "/health"
  }
}
```

#### List Deployments
```http
GET /api/v1/integrations/deployments?project_id=uuid&environment=production&status=success
Authorization: Bearer <access_token>
```

#### Rollback Deployment
```http
POST /api/v1/integrations/deployments/{deployment_id}/rollback
Authorization: Bearer <access_token>
```

### Dashboard & Analytics Endpoints

#### Dashboard Overview
```http
GET /api/v1/dashboard/overview?project_id=uuid
Authorization: Bearer <access_token>
```

#### Automation Metrics
```http
GET /api/v1/dashboard/metrics/automation?project_id=uuid
Authorization: Bearer <access_token>
```

#### Project Metrics
```http
GET /api/v1/dashboard/metrics/projects?project_id=uuid
Authorization: Bearer <access_token>
```

#### Activity Feed
```http
GET /api/v1/dashboard/activity-feed?project_id=uuid&limit=20
Authorization: Bearer <access_token>
```

#### Trends Analytics
```http
GET /api/v1/dashboard/analytics/trends?project_id=uuid&days=30
Authorization: Bearer <access_token>
```

## 🔄 Core Workflows

### 1. Requirement to Deployment Flow
```
1. BA inputs requirement → POST /api/v1/requirements
2. AI analyzes requirement → POST /api/v1/requirements/{id}/analyze
3. Generate tasks → POST /api/v1/requirements/{id}/generate-tasks
4. AI agent executes → POST /api/v1/agents/{id}/execute
5. Human review → POST /api/v1/agents/actions/{id}/approve
6. Deploy → POST /api/v1/integrations/deployments
```

### 2. AI Agent Decision Process
```
1. Agent receives task
2. Analyzes context and dependencies
3. Generates solution with confidence score
4. If confidence > threshold: Execute autonomously
5. If confidence < threshold: Escalate for human review
6. Log all actions for audit trail
```

## 📊 Response Examples

### Successful Response
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "AI Chat Platform",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Error Response
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Dashboard Overview Response
```json
{
  "projects": {
    "total": 10,
    "active": 7,
    "completion_rate": 73.5
  },
  "tasks": {
    "total": 245,
    "completed": 180,
    "pending": 45,
    "completion_rate": 73.5
  },
  "ai_automation": {
    "active_agents": 12,
    "total_actions": 1520,
    "pending_reviews": 8,
    "automation_rate": 87.3
  },
  "quick_stats": {
    "tasks_completed_today": 15,
    "deployments_this_week": 8,
    "ai_decisions_made": 245
  }
}
```

## 🚨 Error Handling

### HTTP Status Codes
- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

### Error Response Format
```json
{
  "detail": "Error description",
  "error_code": "SPECIFIC_ERROR_CODE",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🔒 Security Features

### Authentication & Authorization
- JWT token-based authentication
- Role-based access control (RBAC)
- Permission-based resource access
- Token refresh mechanism

### Data Protection
- Password hashing with bcrypt
- Sensitive data encryption
- API rate limiting
- Input validation and sanitization

### Audit & Compliance
- Complete audit trail
- Security event logging
- Access monitoring
- Compliance reporting

## 🚀 Performance Features

### Caching
- Redis-based caching
- Query result caching
- Session management

### Database Optimization
- Async database operations
- Connection pooling
- Query optimization
- Database indexing

### Rate Limiting
- Per-user rate limiting
- Endpoint-specific limits
- Burst protection

## 🧪 Testing

### API Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app
```

### Manual Testing
Use the provided Postman collection for comprehensive API testing.

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the error logs for debugging

---

**TechSophy Keystone** - Transforming software development with AI-powered automation.
