---
name: python-test-generator
description: Generate comprehensive Python test suites with pytest, async support, mocking for LLM APIs, and FastAPI/SQLAlchemy fixtures. This skill should be used when writing tests, setting up test infrastructure, or generating test cases for Python projects.
---

# Python Test Generator Skill

## Overview

This skill generates comprehensive Python test suites using pytest with async support, mocks for external APIs (OpenAI, Anthropic, Google), fixture patterns for FastAPI and SQLAlchemy, coverage configuration, and parameterized test generation.

## When to Use This Skill

- Writing tests for a new feature or module
- Setting up test infrastructure for a project
- Mocking LLM API calls in tests
- Creating FastAPI integration tests
- Generating parameterized test cases
- Setting up coverage targets

## Test Project Setup

### `pyproject.toml` Configuration

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow running",
    "integration: marks tests requiring external services",
]

[tool.coverage.run]
source = ["app"]
omit = ["*/tests/*", "*/migrations/*"]

[tool.coverage.report]
fail_under = 80
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.",
]
```

### `requirements-test.txt`

```
pytest>=8.0
pytest-asyncio>=0.23
pytest-cov>=4.1
pytest-mock>=3.12
httpx>=0.27
respx>=0.21
factory-boy>=3.3
faker>=22.0
freezegun>=1.3
```

## Core Fixtures

### `tests/conftest.py` - FastAPI + Async SQLAlchemy

```python
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.main import app
from app.database import get_db
from app.models.base import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(autouse=True)
async def setup_db():
    """Create tables before each test, drop after."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session():
    """Provide a transactional database session."""
    async with TestSession() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(db_session):
    """Async test client with DB override."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers():
    """Generate valid auth headers for testing."""
    from app.services.auth import create_access_token
    token = create_access_token(subject="test-user-id")
    return {"Authorization": f"Bearer {token}"}
```

## Mocking LLM APIs

### Mock Anthropic (Claude)

```python
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

@pytest.fixture
def mock_anthropic():
    """Mock Anthropic client."""
    with patch("app.services.llm.Anthropic") as mock_cls:
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        # Mock messages.create
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Mocked response")]
        mock_response.usage.input_tokens = 100
        mock_response.usage.output_tokens = 50
        mock_client.messages.create.return_value = mock_response

        yield mock_client


# Async variant
@pytest.fixture
def mock_anthropic_async():
    with patch("app.services.llm.AsyncAnthropic") as mock_cls:
        mock_client = AsyncMock()
        mock_cls.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Mocked response")]
        mock_client.messages.create.return_value = mock_response

        yield mock_client
```

### Mock OpenAI

```python
@pytest.fixture
def mock_openai():
    """Mock OpenAI client."""
    with patch("app.services.llm.OpenAI") as mock_cls:
        mock_client = MagicMock()
        mock_cls.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Mocked response"))
        ]
        mock_response.usage.total_tokens = 150
        mock_client.chat.completions.create.return_value = mock_response

        yield mock_client
```

### Mock Embeddings

```python
import numpy as np

@pytest.fixture
def mock_embeddings():
    """Mock embedding model returning deterministic vectors."""
    with patch("app.services.rag.OpenAIEmbeddings") as mock_cls:
        mock_embed = MagicMock()
        mock_embed.embed_documents.return_value = [
            np.random.rand(1536).tolist() for _ in range(10)
        ]
        mock_embed.embed_query.return_value = np.random.rand(1536).tolist()
        mock_cls.return_value = mock_embed
        yield mock_embed
```

## Test Patterns

### FastAPI Endpoint Tests

```python
import pytest

class TestUserEndpoints:
    async def test_create_user(self, client, auth_headers):
        response = await client.post(
            "/api/v1/users",
            json={"email": "new@example.com", "name": "Test User"},
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@example.com"

    async def test_create_user_duplicate_email(self, client, auth_headers, db_session):
        # Setup: create existing user
        from app.models.user import User
        user = User(email="exists@example.com", name="Existing")
        db_session.add(user)
        await db_session.commit()

        response = await client.post(
            "/api/v1/users",
            json={"email": "exists@example.com", "name": "Duplicate"},
            headers=auth_headers,
        )
        assert response.status_code == 409

    async def test_create_user_unauthorized(self, client):
        response = await client.post(
            "/api/v1/users",
            json={"email": "new@example.com", "name": "Test"},
        )
        assert response.status_code == 401
```

### Service Layer Tests

```python
class TestUserService:
    async def test_get_user_by_email(self, db_session):
        from app.services.user import UserService
        from app.models.user import User

        user = User(email="test@example.com", name="Test")
        db_session.add(user)
        await db_session.commit()

        service = UserService(db_session)
        result = await service.get_by_email("test@example.com")
        assert result is not None
        assert result.name == "Test"

    async def test_get_user_not_found(self, db_session):
        from app.services.user import UserService

        service = UserService(db_session)
        result = await service.get_by_email("nonexistent@example.com")
        assert result is None
```

### Parameterized Tests

```python
import pytest

@pytest.mark.parametrize("input_text,expected_sentiment", [
    ("I love this product!", "positive"),
    ("This is terrible", "negative"),
    ("It's okay I guess", "neutral"),
    ("", "neutral"),
    ("Best purchase ever! Highly recommend!", "positive"),
])
async def test_sentiment_analysis(mock_anthropic, input_text, expected_sentiment):
    from app.services.analysis import analyze_sentiment

    mock_anthropic.messages.create.return_value.content[0].text = expected_sentiment
    result = await analyze_sentiment(input_text)
    assert result == expected_sentiment


@pytest.mark.parametrize("status_code,expected_error", [
    (400, "Bad Request"),
    (401, "Unauthorized"),
    (403, "Forbidden"),
    (404, "Not Found"),
    (500, "Internal Server Error"),
])
async def test_error_responses(client, status_code, expected_error):
    # Test error handling for each status code
    ...
```

### Testing with freezegun

```python
from freezegun import freeze_time

@freeze_time("2025-01-15 12:00:00")
async def test_token_expiry(client):
    from app.services.auth import create_access_token
    from datetime import timedelta

    token = create_access_token("user-id", expires_delta=timedelta(hours=1))
    # Token is valid at creation time
    ...

@freeze_time("2025-01-15 14:00:00")
async def test_token_expired(client):
    # Same token is now expired
    ...
```

## Factory Pattern

```python
# tests/factories.py
import factory
from faker import Faker
from app.models.user import User

fake = Faker()

class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.LazyFunction(fake.email)
    name = factory.LazyFunction(fake.name)
    is_active = True
```

## Coverage Commands

```bash
# Run tests with coverage
pytest --cov=app --cov-report=term-missing

# Generate HTML report
pytest --cov=app --cov-report=html

# Fail if coverage below threshold
pytest --cov=app --cov-fail-under=80

# Run only specific markers
pytest -m "not slow"
pytest -m "integration"
```

## Test Generation Checklist

When generating tests for a module:

- [ ] Happy path for each public function/endpoint
- [ ] Error cases (invalid input, missing data, unauthorized)
- [ ] Edge cases (empty input, very large input, special characters)
- [ ] Async behavior (concurrent calls, timeouts)
- [ ] Database constraints (unique, foreign key, not null)
- [ ] Authentication and authorization variants
- [ ] Parameterized tests for similar logic with different inputs
