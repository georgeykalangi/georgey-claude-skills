---
name: docker-deploy
description: Docker and deployment workflows including multi-stage builds, docker-compose for multiple environments, Kubernetes manifests, health checks, and LLM-specific scaling patterns. This skill should be used when containerizing applications, setting up deployment pipelines, or writing K8s manifests.
---

# Docker Deploy Skill

## Overview

This skill covers Docker and deployment workflows for containerized applications, including multi-stage Dockerfile optimization, docker-compose for dev/staging/prod, Kubernetes manifest generation, health checks, observability, and LLM-specific scaling patterns.

## When to Use This Skill

- Containerizing a new application
- Optimizing Docker image size or build time
- Setting up docker-compose for multiple environments
- Generating Kubernetes manifests
- Adding health checks and monitoring
- Deploying LLM-powered applications
- Configuring CI/CD pipelines

## Multi-Stage Dockerfile

### Python (FastAPI)

```dockerfile
# Stage 1: Dependencies
FROM python:3.12-slim AS dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Production
FROM python:3.12-slim AS production
WORKDIR /app

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy installed packages
COPY --from=dependencies /install /usr/local

# Copy application code
COPY app/ ./app/

# Switch to non-root user
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Node.js (Next.js)

```dockerfile
FROM node:20-alpine AS dependencies
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production

FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS production
WORKDIR /app
ENV NODE_ENV=production

RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001

COPY --from=dependencies /app/node_modules ./node_modules
COPY --from=build /app/.next ./.next
COPY --from=build /app/public ./public
COPY --from=build /app/package.json ./

USER appuser
EXPOSE 3000

CMD ["npm", "start"]
```

### Image Optimization Tips

| Technique | Impact |
|-----------|--------|
| Multi-stage builds | 50-80% size reduction |
| `-slim` / `-alpine` base | 60-90% base size reduction |
| `--no-cache-dir` for pip | 10-20% reduction |
| `.dockerignore` | Faster builds, smaller context |
| Layer ordering (deps first) | Faster rebuilds via cache |
| Non-root user | Security best practice |

### `.dockerignore`

```
.git
.env
.env.*
__pycache__
*.pyc
.pytest_cache
.coverage
htmlcov
node_modules
.next
*.md
!README.md
```

## Docker Compose Environments

### `docker-compose.yml` (Development)

```yaml
services:
  api:
    build:
      context: .
      target: dependencies
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    env_file: .env
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-postgres}
      POSTGRES_DB: ${DB_NAME:-appdb}
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

### `docker-compose.prod.yml` (Production Override)

```yaml
services:
  api:
    build:
      context: .
      target: production
    ports:
      - "8000:8000"
    volumes: []  # No bind mounts in prod
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
    restart: always
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  db:
    volumes:
      - pgdata:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 2G
```

**Run commands:**
```bash
# Development
docker compose up

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Staging
docker compose -f docker-compose.yml -f docker-compose.staging.yml up -d
```

## Kubernetes Manifests

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
  labels:
    app: api-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-server
  template:
    metadata:
      labels:
        app: api-server
    spec:
      containers:
        - name: api
          image: registry.example.com/api-server:latest
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: api-config
            - secretRef:
                name: api-secrets
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 15
            periodSeconds: 20
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
```

### Service + Ingress

```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-server
spec:
  selector:
    app: api-server
  ports:
    - port: 80
      targetPort: 8000
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - api.example.com
      secretName: api-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-server
                port:
                  number: 80
```

### ConfigMap + Secret

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
data:
  PROJECT_NAME: "my-service"
  LOG_LEVEL: "info"
  ALLOWED_ORIGINS: "https://app.example.com"
---
apiVersion: v1
kind: Secret
metadata:
  name: api-secrets
type: Opaque
stringData:
  DATABASE_URL: "postgresql+asyncpg://user:pass@db:5432/appdb"
  SECRET_KEY: "change-in-production"
  OPENAI_API_KEY: "sk-..."
```

## Health Checks

### FastAPI Health Endpoint

```python
from fastapi import APIRouter, status
from sqlalchemy import text
from app.database import async_session

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    checks = {"status": "healthy", "checks": {}}

    # Database check
    try:
        async with async_session() as session:
            await session.execute(text("SELECT 1"))
        checks["checks"]["database"] = "ok"
    except Exception as e:
        checks["status"] = "unhealthy"
        checks["checks"]["database"] = str(e)

    status_code = 200 if checks["status"] == "healthy" else 503
    return checks
```

## LLM-Specific Scaling Patterns

### GPU Pod Configuration

```yaml
# For self-hosted models (vLLM, Ollama)
spec:
  containers:
    - name: llm-server
      image: vllm/vllm-openai:latest
      resources:
        limits:
          nvidia.com/gpu: 1
          memory: "16Gi"
        requests:
          nvidia.com/gpu: 1
          memory: "8Gi"
  nodeSelector:
    gpu: "true"
  tolerations:
    - key: nvidia.com/gpu
      operator: Exists
      effect: NoSchedule
```

### Request Queue Pattern

```yaml
# Separate API server from LLM worker
services:
  api:
    build: .
    environment:
      - REDIS_URL=redis://redis:6379

  llm-worker:
    build: .
    command: python -m app.workers.llm_worker
    environment:
      - REDIS_URL=redis://redis:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    deploy:
      replicas: 2  # Scale independently from API

  redis:
    image: redis:7-alpine
```

### Cost-Aware Scaling

| Pattern | When to Use |
|---------|------------|
| Queue + workers | High latency tolerance, batch processing |
| Direct API calls | Low latency needed, low volume |
| Caching layer | Repeated similar queries |
| Model routing | Mix of simple/complex queries |

## Deployment Checklist

- [ ] Dockerfile uses multi-stage build
- [ ] Non-root user in container
- [ ] Health checks configured
- [ ] Resource limits set
- [ ] Secrets not in image or env files
- [ ] `.dockerignore` excludes unnecessary files
- [ ] Logging configured (structured JSON)
- [ ] Graceful shutdown handled
