# Keycloak Integration Guide

## 🔐 Authentication Service Migration

Your TechSophy Keystone backend has been successfully migrated from **custom JWT authentication** to **Keycloak integration** for enterprise-grade centralized authentication.

## 📊 Authentication Architecture Comparison

### Before (Custom JWT):
- ❌ Local user management in PostgreSQL
- ❌ Manual JWT token generation/validation
- ❌ Password storage and hashing
- ❌ Limited scalability across multiple services

### After (Keycloak Integration):
- ✅ Centralized authentication server
- ✅ OAuth 2.0 / OpenID Connect support
- ✅ Single Sign-On (SSO) capability
- ✅ Enterprise user federation (LDAP/AD)
- ✅ Advanced security features
- ✅ Multi-application support

## 🚀 Keycloak Setup Instructions

### 1. Install Keycloak with Docker

```bash
# Create Keycloak directory
mkdir keycloak-setup && cd keycloak-setup

# Create docker-compose.yml for Keycloak
cat > docker-compose.yml << EOF
version: '3.8'
services:
  keycloak-db:
    image: postgres:15
    environment:
      POSTGRES_DB: keycloak
      POSTGRES_USER: keycloak
      POSTGRES_PASSWORD: keycloak_password
    volumes:
      - keycloak_db_data:/var/lib/postgresql/data
    networks:
      - keycloak-network

  keycloak:
    image: quay.io/keycloak/keycloak:23.0
    environment:
      KC_DB: postgres
      KC_DB_URL: jdbc:postgresql://keycloak-db:5432/keycloak
      KC_DB_USERNAME: keycloak
      KC_DB_PASSWORD: keycloak_password
      KC_HOSTNAME_STRICT: false
      KC_HOSTNAME_STRICT_HTTPS: false
      KC_HTTP_ENABLED: true
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin
    ports:
      - "8080:8080"
    depends_on:
      - keycloak-db
    command: start-dev
    networks:
      - keycloak-network

volumes:
  keycloak_db_data:

networks:
  keycloak-network:
EOF

# Start Keycloak
docker-compose up -d
```

### 2. Configure Keycloak Realm and Client

1. **Access Keycloak Admin Console**:
   - URL: `http://localhost:8080`
   - Username: `admin`
   - Password: `admin`

2. **Create Realm**:
   - Click "Create Realm"
   - Name: `techsophy`
   - Enable: `true`
   - Click "Create"

3. **Create Client**:
   - Go to Clients → Create Client
   - Client type: `OpenID Connect`
   - Client ID: `keystone-backend`
   - Click "Next"
   
   **Capability config**:
   - Client authentication: `ON`
   - Authorization: `OFF`
   - Standard flow: `ON`
   - Direct access grants: `ON`
   - Click "Next"
   
   **Login settings**:
   - Valid redirect URIs: `http://localhost:3000/*`
   - Web origins: `http://localhost:3000`
   - Click "Save"

4. **Get Client Secret**:
   - Go to Clients → keystone-backend → Credentials
   - Copy the "Client secret"

### 3. Configure User Roles (Optional)

```bash
# Create roles for your application
1. Go to Realm roles → Create role
2. Create these roles:
   - project_manager
   - business_analyst
   - developer
   - reviewer
   - admin
```

## 🔧 Environment Configuration

Create or update your `.env` file:

```bash
# Application
PROJECT_NAME=TechSophy Keystone API
ENVIRONMENT=development
DEBUG=true

# Authentication Mode
AUTH_MODE=keycloak

# Keycloak Configuration
KEYCLOAK_URL=http://localhost:8080
KEYCLOAK_REALM=techsophy
KEYCLOAK_CLIENT_ID=keystone-backend
KEYCLOAK_CLIENT_SECRET=your_client_secret_here
KEYCLOAK_ADMIN_USERNAME=admin
KEYCLOAK_ADMIN_PASSWORD=admin

# Database
DATABASE_URL=postgresql://user:password@localhost/keystone_db

# Redis
REDIS_URL=redis://localhost:6379

# Google AI
GOOGLE_AI_API_KEY=your_gemini_api_key

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

## 🔄 Migration Process

### For Existing Users:
1. **Export existing users** from your current database
2. **Import users to Keycloak** using Admin API or Keycloak Admin Console
3. **Map user roles** to Keycloak roles
4. **Update user passwords** (users will need to reset passwords)

### Database Changes:
- Local user authentication is maintained as fallback
- User sync occurs automatically when users login via Keycloak
- Existing user records are updated with Keycloak info

## 📡 Updated API Endpoints

### Authentication Flow with Keycloak:

```bash
# 1. Register User (creates in both Keycloak and local DB)
POST /api/v1/auth/register
{
  "username": "john_doe",
  "email": "john@techsophy.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "SecurePassword123!"
}

# 2. Login (authenticates with Keycloak)
POST /api/v1/auth/login
{
  "username": "john_doe",
  "password": "SecurePassword123!"
}

# Response includes Keycloak tokens:
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer"
}

# 3. Use token for API calls
GET /api/v1/auth/me
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...

# 4. Refresh token
POST /api/v1/auth/refresh
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

# 5. Logout (invalidates Keycloak session)
POST /api/v1/auth/logout
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## 🔒 Security Features

### Token Validation:
- **RS256 Algorithm**: Keycloak uses RSA public key cryptography
- **JWK Endpoint**: Public keys fetched automatically from Keycloak
- **Token Expiration**: Configurable token lifetimes
- **Audience Validation**: Ensures tokens are for your application

### User Sync:
- **Automatic Sync**: Users synced to local DB on first login
- **Profile Updates**: User info updated from Keycloak on each login
- **Role Mapping**: Keycloak roles mapped to application permissions

## 🚦 Testing Keycloak Integration

### 1. Test with Postman:
- Import the provided Postman collection
- The authentication endpoints now work with Keycloak
- Tokens are Keycloak JWT tokens (longer format)

### 2. Test User Flow:
```bash
# Register a test user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@techsophy.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "TestPassword123!"
  }'

# Login with Keycloak
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPassword123!"
  }'
```

## 🎛️ Configuration Modes

### Switch Authentication Modes:
```bash
# Use Keycloak (Production)
AUTH_MODE=keycloak

# Use Local JWT (Development/Fallback)
AUTH_MODE=local
```

## 🚀 Production Deployment

### Environment Variables for Production:
```bash
# Production Keycloak URL
KEYCLOAK_URL=https://keycloak.yourcompany.com

# Production Realm
KEYCLOAK_REALM=production

# Secure Client Secret
KEYCLOAK_CLIENT_SECRET=super_secure_client_secret

# Production Database
DATABASE_URL=postgresql://prod_user:prod_pass@prod_db:5432/keystone_prod
```

## 🔧 Troubleshooting

### Common Issues:

1. **Connection Error**:
   ```bash
   # Check Keycloak is running
   curl http://localhost:8080/health
   ```

2. **Token Validation Failed**:
   - Verify client secret is correct
   - Check realm name matches configuration
   - Ensure Keycloak is accessible

3. **User Creation Failed**:
   - Check admin credentials
   - Verify realm permissions
   - Check network connectivity

## 📊 Benefits of Keycloak Integration

### For Development:
- ✅ Centralized user management
- ✅ OAuth 2.0 / OpenID Connect standards
- ✅ Easy integration with frontend applications
- ✅ Built-in admin interface

### For Production:
- ✅ Enterprise-grade security
- ✅ Single Sign-On across applications
- ✅ LDAP/Active Directory integration
- ✅ Scalable multi-tenant architecture
- ✅ Compliance with security standards

Your TechSophy Keystone backend is now ready for enterprise deployment with Keycloak authentication! 🚀
