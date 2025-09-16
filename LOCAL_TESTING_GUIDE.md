# 🚀 Local Testing Guide - TechSophy Keystone API

## 📋 Pre-Testing Checklist

### 1. Environment Setup
Create your `.env` file in the project root:

```bash
# Application Configuration
PROJECT_NAME=TechSophy Keystone API
ENVIRONMENT=development
DEBUG=true

# Authentication Mode (Choose one)
AUTH_MODE=local  # For quick local testing without Keycloak
# AUTH_MODE=keycloak  # For full Keycloak integration testing

# Local JWT Settings (for AUTH_MODE=local)
SECRET_KEY=your-super-secret-key-here-32-chars-min
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Keycloak Configuration (for AUTH_MODE=keycloak)
KEYCLOAK_URL=http://localhost:8080
KEYCLOAK_REALM=techsophy
KEYCLOAK_CLIENT_ID=keystone-backend
KEYCLOAK_CLIENT_SECRET=your_client_secret_here
KEYCLOAK_ADMIN_USERNAME=admin
KEYCLOAK_ADMIN_PASSWORD=admin

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/keystone_db
# Alternative SQLite for quick testing:
# DATABASE_URL=sqlite+aiosqlite:///./keystone.db

# Redis
REDIS_URL=redis://localhost:6379

# Google AI
GOOGLE_AI_API_KEY=your_gemini_api_key_here

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 2. Database Setup

#### Option A: PostgreSQL (Recommended)
```bash
# Install and start PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres createuser --interactive
sudo -u postgres createdb keystone_db

# Set password
sudo -u postgres psql
ALTER USER postgres PASSWORD 'password';
\q
```

#### Option B: SQLite (Quick Testing)
```bash
# No setup needed - just use SQLite URL in .env
DATABASE_URL=sqlite+aiosqlite:///./keystone.db
```

### 3. Redis Setup
```bash
# Install Redis
sudo apt install redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Test Redis
redis-cli ping  # Should return PONG
```

## 🏃‍♂️ Quick Start (5 minutes)

### 1. Install Dependencies
```bash
cd /home/younus/Documents/keystone-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the Application
```bash
# Method 1: Direct run
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Method 2: Using provided script
chmod +x scripts/run.sh
./scripts/run.sh

# Method 3: Using Docker
docker-compose up --build
```

### 3. Verify Application is Running
```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "timestamp": "2024-01-15T10:30:00Z"}
```

### 4. Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📨 Postman Testing Sequence

### Import Collection
1. Open Postman
2. Click "Import" → "Upload Files"
3. Select: `/home/younus/Documents/keystone-backend/TechSophy_Keystone_Postman_Collection.json`
4. Click "Import"

### Set Collection Variables
In Postman, go to your collection → Variables tab:
- `base_url`: `http://localhost:8000`
- `keycloak_url`: `http://localhost:8080` (if using Keycloak)

## 🧪 Testing Scenarios

### Scenario 1: Quick API Testing (Local Auth)
**Duration**: 5 minutes
**Prerequisites**: Application running with `AUTH_MODE=local`

```bash
# Test sequence in Postman:
1. Authentication → Register User
2. Authentication → Login
3. Authentication → Get Current User
4. Projects → Create Project
5. Requirements → Create Requirement
6. Tasks → Create Task
7. Dashboard → Dashboard Overview
```

### Scenario 2: Full SDLC Workflow Testing
**Duration**: 15 minutes
**Prerequisites**: Application running, database connected

```bash
# Complete workflow in Postman:
1. Register User (john_doe)
2. Login (get access token)
3. Create Project (AI Chat Platform)
4. Create Requirement (User Authentication System)
5. AI Analyze Requirement
6. Generate Tasks from Requirement
7. Create AI Agent (CodeGen Agent)
8. Execute Agent Action (Code Generation)
9. Get Agent Actions (Review pending actions)
10. Approve Agent Action
11. Create GitHub Integration
12. Create Deployment
13. Dashboard Overview (View metrics)
14. Activity Feed (See all activities)
```

### Scenario 3: Keycloak Integration Testing
**Duration**: 20 minutes
**Prerequisites**: Keycloak running, realm configured

```bash
# Setup Keycloak first:
1. Start Keycloak: docker-compose -f keycloak-setup/docker-compose.yml up -d
2. Configure realm and client (see KEYCLOAK_SETUP.md)
3. Set AUTH_MODE=keycloak in .env
4. Restart application

# Test sequence:
1. Register User (creates in Keycloak + local DB)
2. Login (authenticates with Keycloak)
3. Verify token is Keycloak JWT (longer format)
4. Continue with full workflow
5. Test token refresh
6. Test logout
```

## 📊 Expected Test Results

### Successful Registration Response:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "john.doe@techsophy.com",
  "username": "john_doe",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Successful Login Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Dashboard Overview Response:
```json
{
  "projects": {
    "total": 1,
    "active": 1,
    "completion_rate": 25.0
  },
  "tasks": {
    "total": 3,
    "completed": 0,
    "pending": 3,
    "completion_rate": 0.0
  },
  "ai_automation": {
    "active_agents": 1,
    "total_actions": 1,
    "pending_reviews": 1,
    "automation_rate": 85.0
  }
}
```

## 🔧 Troubleshooting

### Common Issues:

#### 1. Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -h localhost -U postgres -d keystone_db

# Solution: Update DATABASE_URL in .env
```

#### 2. Redis Connection Error
```bash
# Check Redis is running
sudo systemctl status redis-server

# Test connection
redis-cli ping

# Solution: Start Redis or update REDIS_URL
```

#### 3. Import Errors
```bash
# Missing dependencies
pip install -r requirements.txt

# Python path issues
export PYTHONPATH=/home/younus/Documents/keystone-backend:$PYTHONPATH
```

#### 4. Port Already in Use
```bash
# Check what's using port 8000
sudo lsof -i :8000

# Kill process or use different port
uvicorn app.main:app --reload --port 8001
```

#### 5. Keycloak Connection Issues
```bash
# Check Keycloak is running
curl http://localhost:8080/health

# Check realm exists
curl http://localhost:8080/realms/techsophy

# Verify client configuration in Keycloak admin console
```

## 📈 Performance Testing

### Load Testing with curl:
```bash
# Test concurrent requests
for i in {1..10}; do
  curl -X GET "http://localhost:8000/api/v1/auth/me" \
    -H "Authorization: Bearer YOUR_TOKEN" &
done
wait
```

### Memory and CPU Monitoring:
```bash
# Monitor application resources
top -p $(pgrep -f "uvicorn")

# Monitor database connections
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"
```

## ✅ Test Completion Checklist

- [ ] Application starts without errors
- [ ] Database connection established
- [ ] Redis connection working
- [ ] User registration successful
- [ ] User login successful
- [ ] JWT token validation working
- [ ] Project creation successful
- [ ] Requirements management working
- [ ] AI agents functioning
- [ ] Task management working
- [ ] Integrations working
- [ ] Dashboard displaying metrics
- [ ] All API endpoints responding correctly

## 🚀 Ready for Dev Instance Testing

Once local testing is successful:

1. ✅ **Confirm all endpoints work locally**
2. ✅ **Verify authentication flow**
3. ✅ **Test complete SDLC workflow**
4. ✅ **Validate AI agent functionality**
5. ✅ **Check dashboard metrics**

**You're now ready to provide the dev instance URLs for production testing!**

---

**Next Steps**: After successful local testing, provide your dev instance API gateway and auth URLs, and I'll update the collection for production testing.
