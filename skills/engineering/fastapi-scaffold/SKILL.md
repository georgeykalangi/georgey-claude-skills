---
name: fastapi-scaffold
description: Scaffold new FastAPI projects with async SQLAlchemy, Pydantic v2, JWT auth, Docker, and Alembic migrations. This skill should be used when starting a new FastAPI project, setting up API boilerplate, or creating backend service scaffolding.
---

# FastAPI Scaffold Skill

## Overview

This skill scaffolds production-ready FastAPI projects with Georgey's preferred patterns: async SQLAlchemy + PostgreSQL, Pydantic v2 models, JWT authentication, CORS configuration, Docker + docker-compose, and Alembic migrations.

## When to Use This Skill

- Starting a new FastAPI backend project
- Setting up API boilerplate with auth
- Creating microservice scaffolding
- Generating project structure for a new service
- Adding Docker configuration to an existing FastAPI project

## Project Structure

```
project_name/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Settings via pydantic-settings
│   ├── database.py             # Async SQLAlchemy engine/session
│   ├── dependencies.py         # Shared dependencies (get_db, get_current_user)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py             # Login, register, refresh token
│   │   ├── users.py            # User CRUD
│   │   └── health.py           # Health check endpoint
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py             # Declarative base + mixins
│   │   └── user.py             # User ORM model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py             # Token, login request/response
│   │   └── user.py             # User create/read/update
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py             # JWT creation, password hashing
│   │   └── user.py             # User business logic
│   └── middleware/
│       ├── __init__.py
│       └── cors.py             # CORS configuration
├── alembic/
│   ├── env.py
│   ├── versions/
│   └── alembic.ini
├── tests/
│   ├── conftest.py             # Fixtures (async client, test db)
│   ├── test_auth.py
│   └── test_users.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Key Files

### `app/main.py`

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.routers import auth, users, health
from app.middleware.cors import add_cors

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

add_cors(app)
app.include_router(health.router, tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
```

### `app/config.py`

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "my-service"
    VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/dbname"

    # Auth
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env"}

settings = Settings()
```

### `app/database.py`

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### `app/models/base.py`

```python
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
```

### `app/services/auth.py`

```python
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return jwt.encode(
        {"sub": subject, "exp": expire},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
```

### `Dockerfile`

```dockerfile
FROM python:3.12-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS production
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `docker-compose.yml`

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app

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

volumes:
  pgdata:
```

### `requirements.txt`

```
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
sqlalchemy[asyncio]>=2.0
asyncpg>=0.29.0
pydantic-settings>=2.0
python-jose[cryptography]>=3.3
passlib[bcrypt]>=1.7
alembic>=1.13
python-multipart>=0.0.6
httpx>=0.27.0
```

## Alembic Setup

```bash
# Initialize alembic
alembic init alembic

# Update alembic/env.py to use async engine
# Generate first migration
alembic revision --autogenerate -m "initial"

# Apply migrations
alembic upgrade head
```

**Key `alembic/env.py` change** - use async engine:

```python
from app.database import engine
from app.models.base import Base

target_metadata = Base.metadata

async def run_async_migrations():
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()
```

## Scaffold Commands

When scaffolding a new project:

1. Create the directory structure above
2. Generate all boilerplate files
3. Initialize Alembic with async config
4. Create `.env.example` with all required variables
5. Verify with `docker-compose up --build`

## Customization Points

| Component | Options |
|-----------|---------|
| **Database** | PostgreSQL (default), SQLite for dev |
| **Auth** | JWT (default), OAuth2, API key |
| **ORM** | SQLAlchemy async (default) |
| **Migrations** | Alembic (default) |
| **Server** | Uvicorn (default), Gunicorn + Uvicorn workers |
