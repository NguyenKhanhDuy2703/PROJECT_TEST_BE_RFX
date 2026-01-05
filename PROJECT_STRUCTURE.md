# Project Structure

```
be-assignment.jan-2026/
├── README.md
├── .gitignore
├── .dockerignore
├── .env.example
├── Justfile
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
│
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── config.py                  # Configuration settings
│   │
│   ├── core/                      # Core utilities
│   │   ├── __init__.py
│   │   ├── security.py           # JWT, password hashing
│   │   ├── auth.py                # Authentication & authorization
│   │   ├── exceptions.py          # Custom exceptions
│   │   └── logging.py              # Logging configuration
│   │
│   ├── db/                        # Database setup
│   │   ├── __init__.py
│   │   ├── base.py                # Base model class
│   │   └── session.py              # Database session management
│   │
│   ├── models/                    # SQLAlchemy models
│   │   ├── __init__.py
│   │
│   ├── schemas/                   # Pydantic schemas
│   │   ├── __init__.py
│   │   └── common.py               # Common schemas (pagination, etc.)
│   │
│   ├── api/                       # API routes
│   │   ├── __init__.py
│   │   └── v1/                    # API version 1
│   │       ├── __init__.py
│   │       ├── auth.py            # Authentication endpoints
│   │       └── health.py           # Health check endpoint
│   │
│   ├── services/                  # Business logic layer
│   │   ├── __init__.py
│   │   └── redis_service.py        # Redis caching & notifications
│   │
│   ├── utils/                     # Utility functions
│   │   ├── __init__.py
│   │   └── file_upload.py          # File upload handling
│   │
│   ├── mcp/                       # MCP Server
│   │   ├── __init__.py
│   │   ├── server.py               # MCP server setup
│   │   └── converter.py            # FastAPI to MCP auto-conversion
│   │
│   └── agent/                     # Task AI Agent
│       ├── __init__.py
│       ├── agent.py                # Main agent logic
│
├── migrations/                    # Alembic database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/                   # Migration versions
│       └── .gitkeep
│
├── tests/                         # Test files
│   ├── __init__.py
│   ├── conftest.py                 # Pytest configuration & fixtures
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_organizations.py
│   ├── test_projects.py
│   ├── test_tasks.py
│   ├── test_mcp.py                 # MCP server tests
│   └── test_agent.py                # AI Agent tests
│
├── nginx/                         # Nginx configuration
│   └── nginx.conf
│
├── docs/                          # Documentation
│   ├── ER_diagram.md               # Entity Relationship diagram
│   └── system_design.md            # System design diagram
│
└── storage/                       # File storage
    └── uploads/                    # Uploaded attachments
        └── .gitkeep
```

## Key Directories

- **app/**: Main application code organized by concerns (models, schemas, API, services)
- **migrations/**: Database migration files using Alembic
- **tests/**: Test suite with pytest
- **nginx/**: Nginx reverse proxy configuration
- **docs/**: ER diagram and system design documentation
- **storage/**: Local file storage for attachments

