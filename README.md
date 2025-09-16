# TechSophy Keystone API - README

## 🚀 AI-Powered SDLC Management Platform

TechSophy Keystone is a comprehensive Software Development Lifecycle (SDLC) Management Platform that leverages AI to automate and streamline the entire software development process.

## ✨ Features

- **User Authentication & Authorization**: JWT-based secure authentication system
- **Project Management**: Complete CRUD operations for project lifecycle management
- **Requirements Management**: Advanced requirements tracking with AI analysis
- **AI-Powered Analysis**: Intelligent requirement analysis using Google Gemini AI
- **Task Generation**: Automatic task generation from requirements using AI
- **Real-time API**: RESTful API with comprehensive validation and error handling

## 🛠 Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with async SQLAlchemy
- **Caching**: Redis
- **AI Integration**: Google Gemini AI
- **Authentication**: JWT tokens with refresh mechanism
- **Containerization**: Docker & Docker Compose
- **API Documentation**: OpenAPI/Swagger

## 📋 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/refresh` - Refresh access token

### Projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects` - List projects (paginated)
- `GET /api/v1/projects/{id}` - Get project details
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

### Requirements
- `POST /api/v1/requirements` - Create requirement
- `GET /api/v1/requirements/project/{project_id}` - List project requirements
- `GET /api/v1/requirements/{id}` - Get requirement details
- `PUT /api/v1/requirements/{id}` - Update requirement
- `DELETE /api/v1/requirements/{id}` - Delete requirement
- `POST /api/v1/requirements/{id}/analyze` - AI analysis
- `POST /api/v1/requirements/{id}/generate-tasks` - Generate tasks

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone and setup**:
   ```bash
   cd /home/younus/Documents/keystone-backend
   cp .env.example .env
   # Edit .env and add your Gemini API key (optional)
   ```

2. **Start services**:
   ```bash
   docker-compose up -d
   ```

3. **Initialize database**:
   ```bash
   docker-compose --profile migration run --rm migrate
   ```

4. **Access API**:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Health: http://localhost:8000/health

### Manual Setup

1. **Install dependencies**:
   ```bash
   sudo apt install python3.12-venv  # On Ubuntu/Debian
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Setup database**:
   ```bash
   # Install and start PostgreSQL
   sudo apt install postgresql postgresql-contrib
   sudo -u postgres createdb techsophy_keystone
   ```

3. **Run application**:
   ```bash
   ./scripts/run.sh
   # Or manually:
   uvicorn app.main:app --reload
   ```

## 🧪 Testing with Postman

### Import Collection
1. Open Postman
2. Import `postman_collection.json`
3. Set base URL to `http://localhost:8000`

### Test Flow
1. **Register User**: `POST /api/v1/auth/register`
2. **Login**: `POST /api/v1/auth/login` (saves token automatically)
3. **Create Project**: `POST /api/v1/projects`
4. **Create Requirement**: `POST /api/v1/requirements`
5. **Analyze Requirement**: `POST /api/v1/requirements/{id}/analyze`
6. **Generate Tasks**: `POST /api/v1/requirements/{id}/generate-tasks`

## 🔒 Authentication

All protected endpoints require a Bearer token:
```
Authorization: Bearer <your_access_token>
```

Obtain tokens via the login endpoint:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=TestPassword123"
```

## 📊 Validation Features

### Input Validation
- Email format validation
- Password strength (8+ chars, uppercase, lowercase, digit)
- Username length (3-50 characters)
- Required field validation
- Enum value validation for status, priority, etc.

### Security Features
- JWT token authentication
- Password hashing with bcrypt
- User access control for resources
- CORS configuration
- Rate limiting middleware

### Error Handling
- Comprehensive error responses
- HTTP status codes following REST standards
- Detailed validation error messages
- Global exception handling

## 🤖 AI Features

When configured with a Gemini API key, the system provides:
- **Requirement Analysis**: Extract entities, features, complexity assessment
- **Task Generation**: Automatic creation of development tasks
- **Effort Estimation**: AI-powered time estimates
- **Risk Assessment**: Identification of potential challenges

## 📝 Example API Calls

### Register User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "password": "SecurePass123"
  }'
```

### Create Project
```bash
curl -X POST "http://localhost:8000/api/v1/projects" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "E-commerce Platform",
    "description": "Modern e-commerce solution",
    "status": "planning",
    "priority": "high"
  }'
```

## 🏗 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   PostgreSQL    │
│   (Postman)     │◄──►│   Backend       │◄──►│   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Redis Cache   │    │   Gemini AI     │
                       │                 │    │   Service       │
                       └─────────────────┘    └─────────────────┘
```

## 🔧 Configuration

Key environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: JWT signing secret
- `GEMINI_API_KEY`: Google AI API key
- `ENVIRONMENT`: development/production

## 📚 API Documentation

When running in development mode:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🔍 Monitoring

- **Health Check**: `GET /health`
- **Application Logs**: Docker logs or console output
- **Database Status**: Via health check endpoint

## 🚢 Deployment

The application is production-ready with:
- Docker containerization
- Health checks
- Environment-based configuration
- Security middleware
- Comprehensive error handling

For production deployment, update the environment variables and use a production database.

## 📄 License

This project is part of the TechSophy Keystone SDLC Management Platform.

---

**Ready for comprehensive testing with Postman!** 🎯

All endpoints are fully functional with proper validation, authentication, and error handling. The API supports the complete software development lifecycle management workflow.
