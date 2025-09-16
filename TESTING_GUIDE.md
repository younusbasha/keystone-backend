# TechSophy Keystone API - Complete Testing Guide

## Overview
This guide provides step-by-step instructions for testing the TechSophy Keystone API using Postman. The API includes authentication, project management, requirements management, and AI-powered analysis features.

## Prerequisites
- Docker and Docker Compose installed
- Postman application
- Optional: PostgreSQL and Redis for local development

## Quick Start with Docker

### 1. Environment Setup
```bash
# Clone and navigate to the project
cd /home/younus/Documents/keystone-backend

# Copy environment file
cp .env.example .env

# Edit .env file and add your Gemini API key (optional for AI features)
# GEMINI_API_KEY=your-api-key-here
```

### 2. Start Services
```bash
# Start all services (PostgreSQL, Redis, API)
docker-compose up -d

# Check service health
docker-compose ps

# View API logs
docker-compose logs -f api
```

### 3. Initialize Database
```bash
# Run database migrations
docker-compose --profile migration run --rm migrate
```

## API Endpoints Overview

### Base URL: `http://localhost:8000`

### Health Check
- **GET** `/health` - Check API health status

### Authentication (`/api/v1/auth`)
- **POST** `/register` - Register new user
- **POST** `/login` - Login user (returns JWT tokens)
- **POST** `/refresh` - Refresh access token
- **GET** `/me` - Get current user info
- **POST** `/logout` - Logout user

### Projects (`/api/v1/projects`)
- **POST** `/` - Create new project
- **GET** `/` - Get user's projects (paginated)
- **GET** `/{project_id}` - Get specific project
- **PUT** `/{project_id}` - Update project
- **DELETE** `/{project_id}` - Delete project

### Requirements (`/api/v1/requirements`)
- **POST** `/` - Create new requirement
- **GET** `/project/{project_id}` - Get project requirements (paginated)
- **GET** `/{requirement_id}` - Get specific requirement
- **PUT** `/{requirement_id}` - Update requirement
- **DELETE** `/{requirement_id}` - Delete requirement
- **POST** `/{requirement_id}/analyze` - AI analysis of requirement
- **POST** `/{requirement_id}/generate-tasks` - Generate tasks from requirement

## Postman Testing Workflow

### Step 1: Import Collection
1. Open Postman
2. Click "Import" button
3. Select the `postman_collection.json` file
4. The collection will be imported with all endpoints and variables

### Step 2: Set Base URL
- Ensure the collection variable `baseUrl` is set to `http://localhost:8000`

### Step 3: Test Authentication Flow

#### Register a New User
```json
POST /api/v1/auth/register
{
  "email": "test@example.com",
  "username": "testuser",
  "first_name": "Test",
  "last_name": "User",
  "password": "TestPassword123",
  "bio": "Test user for API testing"
}
```

#### Login User
```
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=testuser&password=TestPassword123
```
- This will automatically set the `accessToken` variable for subsequent requests

#### Get Current User Info
```
GET /api/v1/auth/me
Authorization: Bearer {{accessToken}}
```

### Step 4: Test Project Management

#### Create Project
```json
POST /api/v1/projects
Authorization: Bearer {{accessToken}}

{
  "name": "E-commerce Platform",
  "description": "A comprehensive e-commerce platform",
  "status": "planning",
  "priority": "high",
  "budget": 50000.00
}
```
- This will automatically set the `projectId` variable

#### Get All Projects
```
GET /api/v1/projects?skip=0&limit=20
Authorization: Bearer {{accessToken}}
```

#### Update Project
```json
PUT /api/v1/projects/{{projectId}}
Authorization: Bearer {{accessToken}}

{
  "status": "active",
  "description": "Updated description"
}
```

### Step 5: Test Requirements Management

#### Create Requirement
```json
POST /api/v1/requirements
Authorization: Bearer {{accessToken}}

{
  "title": "User Authentication System",
  "description": "Implement comprehensive user authentication with registration, login, logout, password reset, email verification, and OAuth integration.",
  "type": "functional",
  "priority": "high",
  "project_id": {{projectId}},
  "acceptance_criteria": [
    "Users can register with email and password",
    "Users can login with valid credentials",
    "Password reset functionality via email"
  ],
  "tags": ["authentication", "security"]
}
```

#### AI Analysis (Optional - requires Gemini API key)
```
POST /api/v1/requirements/{{requirementId}}/analyze
Authorization: Bearer {{accessToken}}
```

#### Generate Tasks from Requirement
```
POST /api/v1/requirements/{{requirementId}}/generate-tasks
Authorization: Bearer {{accessToken}}
```

## Validation Features

### Input Validation
- Email format validation
- Password strength requirements (8+ chars, uppercase, lowercase, digit)
- Username length validation (3-50 characters)
- Required field validation

### Authentication
- JWT token-based authentication
- Token expiration handling
- Refresh token mechanism
- User access control for resources

### Error Handling
- Comprehensive error responses with details
- HTTP status codes following REST standards
- Validation error details for debugging

## Testing Scenarios

### 1. Authentication Flow
- Register with invalid email → 422 Validation Error
- Register with weak password → 422 Validation Error
- Login with wrong credentials → 401 Unauthorized
- Access protected endpoint without token → 401 Unauthorized
- Use expired token → 401 Unauthorized

### 2. Project Management
- Create project with empty name → 422 Validation Error
- Access another user's project → 404 Not Found
- Update non-existent project → 404 Not Found

### 3. Requirements Management
- Create requirement for non-existent project → 404 Not Found
- Access requirement from another user's project → 404 Not Found
- AI analysis without Gemini API key → Service continues with mock response

## Expected Response Formats

### Success Response (User Registration)
```json
{
  "id": 1,
  "email": "test@example.com",
  "username": "testuser",
  "first_name": "Test",
  "last_name": "User",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-08-07T10:00:00Z",
  "updated_at": "2025-08-07T10:00:00Z"
}
```

### Error Response (Validation)
```json
{
  "error": "Validation Error",
  "message": "Input validation failed",
  "details": [
    {
      "loc": ["body", "password"],
      "msg": "Password must be at least 8 characters long",
      "type": "value_error"
    }
  ]
}
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running: `docker-compose ps`
   - Check database URL in .env file

2. **Authentication Issues**
   - Verify JWT token is included in Authorization header
   - Check token expiration (30 minutes default)

3. **AI Features Not Working**
   - Add Gemini API key to .env file
   - AI endpoints will return mock responses without API key

4. **CORS Issues**
   - API allows all origins in development mode
   - Update CORS settings in production

### Useful Commands
```bash
# View API logs
docker-compose logs -f api

# Restart API service
docker-compose restart api

# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d techsophy_keystone

# Stop all services
docker-compose down

# Clean restart
docker-compose down -v && docker-compose up -d
```

## Production Deployment

For production deployment:
1. Update environment variables in .env
2. Set `ENVIRONMENT=production`
3. Use strong SECRET_KEY
4. Configure proper CORS origins
5. Set up SSL/TLS termination
6. Use production database credentials

The API is now fully functional and ready for comprehensive testing with Postman!
