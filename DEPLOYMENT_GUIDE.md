# TechSophy Keystone Deployment Guide

## 🚀 Production Deployment Options

### Quick Start (Local Development)

```bash
# 1. Clone and setup
git clone https://github.com/younusbasha/keystone-backend.git
cd keystone-backend

# 2. Create environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env with your configuration

# 5. Run the application
uvicorn app.main:app --reload
```

### Docker Development

```bash
# Basic services
docker-compose up -d

# With Keycloak
docker-compose --profile keycloak up -d

# With monitoring
docker-compose --profile monitoring up -d

# Full stack
docker-compose --profile keycloak --profile monitoring up -d
```

### Docker Production

```bash
# Production deployment
docker-compose -f docker-compose.yml --profile production up -d

# Build custom production image
docker build --target production -t keystone-backend:prod .

# Run production container
docker run -d \
  --name keystone-api \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql+asyncpg://user:pass@host:5432/db" \
  -e REDIS_URL="redis://host:6379/0" \
  -e SECRET_KEY="your-production-secret" \
  keystone-backend:prod
```

## 🔧 Configuration Management

### Environment Variables Priority
1. System environment variables (highest)
2. `.env` file
3. Default values in settings.py (lowest)

### Required Environment Variables
- `SECRET_KEY`: Cryptographic secret key
- `DATABASE_URL`: Database connection string
- `REDIS_URL`: Redis connection string (optional)

### Optional but Recommended
- `GEMINI_API_KEY`: For AI features
- `SENTRY_DSN`: For error monitoring
- `SMTP_*`: For email notifications

## 🗄️ Database Setup

### SQLite (Development)
```bash
# Default - no setup required
DATABASE_URL=sqlite+aiosqlite:///./keystone.db
```

### PostgreSQL (Production)
```bash
# 1. Create database
createdb techsophy_keystone

# 2. Set environment variable
export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/techsophy_keystone"

# 3. Run migrations
alembic upgrade head
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🚀 Production Deployment Checklist

### Security
- [ ] Change default `SECRET_KEY`
- [ ] Set secure database passwords
- [ ] Enable HTTPS with SSL certificates
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable audit logging

### Performance
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure Redis for caching
- [ ] Set up load balancer (if needed)
- [ ] Configure CDN for static files
- [ ] Optimize database indices

### Monitoring
- [ ] Set up Sentry for error tracking
- [ ] Configure Prometheus + Grafana
- [ ] Set up log aggregation
- [ ] Configure health checks
- [ ] Set up alerting

### Backup & Recovery
- [ ] Database backup strategy
- [ ] File storage backup
- [ ] Disaster recovery plan
- [ ] Test restore procedures

## 🐳 Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: keystone-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: keystone-backend
  template:
    metadata:
      labels:
        app: keystone-backend
    spec:
      containers:
      - name: keystone-backend
        image: keystone-backend:prod
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: keystone-secrets
              key: database-url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: keystone-secrets
              key: secret-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: keystone-backend-service
spec:
  selector:
    app: keystone-backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

## 📊 Monitoring & Observability

### Health Endpoints
- `GET /health` - Basic health check
- `GET /health/ready` - Readiness probe
- `GET /health/live` - Liveness probe
- `GET /metrics` - Prometheus metrics

### Logging Configuration
```python
# Production logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/keystone/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "json"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    }
}
```

## 🔐 Security Best Practices

### Authentication
- Use strong JWT secrets (256-bit minimum)
- Implement token rotation
- Set appropriate token expiration times
- Use HTTPS only in production

### Database Security
- Use connection pooling
- Enable SSL/TLS for database connections
- Implement row-level security
- Regular security updates

### API Security
- Implement rate limiting
- Use CORS properly
- Validate all inputs
- Sanitize outputs
- Log security events

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.13'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest --cov=app --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to production
      run: |
        # Your deployment script here
        echo "Deploying to production..."
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   ```bash
   # Check database connectivity
   docker-compose logs postgres
   ```

2. **Redis Connection Issues**
   ```bash
   # Check Redis status
   docker-compose logs redis
   ```

3. **High Memory Usage**
   ```bash
   # Monitor memory usage
   docker stats
   ```

4. **Slow Response Times**
   ```bash
   # Check application logs
   docker-compose logs api
   ```

### Performance Tuning

1. **Database Optimization**
   - Add proper indices
   - Use connection pooling
   - Optimize queries

2. **Caching Strategy**
   - Enable Redis caching
   - Cache frequently accessed data
   - Implement cache invalidation

3. **Application Tuning**
   - Adjust worker count
   - Configure async settings
   - Optimize memory usage

---

**This deployment guide ensures your TechSophy Keystone backend is production-ready with enterprise-grade security, monitoring, and scalability.**
