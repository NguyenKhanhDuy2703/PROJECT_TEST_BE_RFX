# 📑 Intern Backend Developer Assignment

- Copyright (c) River Flow Solutions, Jsc. 2026. All rights reserved.
- We only use the submissions for candidates evaluation.

## **A. Instructions**
- Submission:
  - Candidate must fork this repository to a public repo under their name for submission. Notify email `hr@riverflow.solutions` when done.
  - The repository must be public and accessible to the public.
  - Mark the "Review Criteria" items as done when you have completed the requirements.
  - **Note**: If you are concerned about others copying your assignment, you may choose to push your code only on the deadline day. Please note, however, that we check the commit log history to verify contributions.

- Build a **multi-organization Task Management backend** (organizations → projects → tasks) with basic collaboration and notifications.  
- **Stack**: Python, FastAPI, PostgreSQL, Redis, Nginx.
- Use Justfile (https://github.com/casey/just) for all run and development commands.
- Use Docker for deployment.
- Deliverables: GitHub repo, ER + System design diagrams, Dockerized deployment, README.
- **Advanced**: Build a Task AI Agent that integrates with the MCP server and LLM models (Groq, OpenAI, etc.) to test and interact with MCP tools. See section C2 for details. 

---

## **B. Task Management Requirements & Use Cases**

### **B1. Functional Scope**
- **Organizations & Users**
  - Each user belongs to an organization.  
  - Roles: **Admin**, **Manager**, **Member**.  

- **Projects**
  - Belong to one organization.  
  - Can add/remove members.  
  - Admin/Manager can create projects, Members can only participate.  

- **Tasks**
  - CRUD operations.  
  - Belong to a project.  
  - Fields: title, description, status (`todo/in-progress/done`), priority (`low/medium/high`), due_date, assignee.  
  - Status workflow: `todo → in-progress → done` (no complex review step).  

- **Collaboration**
  - Users can comment on tasks.  
  - Users can upload simple file attachments (local storage).  

- **Notifications**
  - Users receive a notification when:  
    - They are assigned a task.  
    - Task status changes.  
    - A comment is added to their task.  

- **Reports (Basic)**
  - Count of tasks by status in a project.  
  - List of overdue tasks.  

---

### **B2. Use Cases**
1. **User Management**
   - Register/login with JWT.  
   - Admin adds users to the organization.  

2. **Project Management**
   - Create/list projects.  
   - Add/remove project members.  

3. **Task Management**
   - Create tasks with title, description, assignee, priority, due date.  
   - Update task status (`todo → in-progress → done`).  
   - List tasks in a project (filter by status, assignee, priority) with pagination support.  

4. **Collaboration**
   - Add comments to tasks.  
   - Upload attachment to a task.  

5. **Notifications**
   - Retrieve unread notifications.  
   - Mark notifications as read.  

6. **Reporting**
   - Get per-project task count by status.  
   - Get overdue tasks in a project.  

---

### **B3. Business Rules**
- Only project members can create or update tasks in that project.  
- Only Admin/Manager can assign tasks to others. Members can assign only to themselves.  
- Due date must be today or in the future (not past).  
- Task status can only progress forward (`todo → in-progress → done`), but not backward.  
- Attachments limited to 5MB each, max 3 per task.  

---

## **C. Tech Requirements**
- **Backend**: Python + FastAPI, SQLAlchemy, Alembic migrations.  
- **Database**: PostgreSQL with foreign keys + indexes.  
- **Cache/Notify**: Redis for caching task lists and storing notifications.  
- **Auth**: JWT (PyJWT) + role-based access (Admin/Manager/Member).  
- **Testing**: pytest with test containers or mocks for PostgreSQL & Redis. Specify your testing approach in the README.  
- **Deployment**: Docker + docker-compose (FastAPI + PostgreSQL + Redis + Nginx).  
- **MCP Server**: Convert FastAPI backend to MCP (Model Context Protocol) server using an auto-conversion approach. The MCP server must automatically discover and expose all FastAPI endpoints as MCP tools without requiring manual tool definitions for each endpoint. You may use packages like `fastmcp`, `mcp-server-fastapi`, or build a custom wrapper that introspects FastAPI routes. The MCP server must be tested using the Task AI Agent (see C2).  
- **AI Agent**: Langchain, langgraph, llama-index, openai, groq, anthropic, etc. (You can use any of these or a custom solution).

---

## **C1. MCP Server Conversion**

### **Requirements**
- Convert the FastAPI backend application to an MCP (Model Context Protocol) server.
- Use an auto-conversion approach (package or custom solution) to automatically expose all FastAPI endpoints as MCP tools.
- **Important**: The conversion must be automatic - do not manually define each tool. The solution should automatically discover FastAPI routes (via introspection) and convert them to MCP tools.
- The MCP server should handle:
  - All CRUD endpoints automatically
- **Testing**: MCP server must be tested using the Task AI Agent (see C2). The AI Agent will call MCP tools to verify functionality.

---

## **C2. Task AI Agent**

### **Overview**
Build an intelligent Task AI Agent that interacts with your task management system through the MCP server and leverages LLM models (Groq, OpenAI, Anthropic, etc.) to provide intelligent task management assistance. The AI Agent is also used to test and verify all MCP tools.

### **Requirements**
- **AI Agent Integration**: Create a Task AI Agent that connects to your MCP server to perform task management operations and test MCP tools.
- **LLM Integration**: Integrate with at least one LLM provider (Groq, OpenAI, Anthropic, etc.) to enable natural language understanding and task automation.
- **MCP Testing**: The agent must be used to test all MCP tools to verify they work correctly.
- **Agent Capabilities**: The agent should be able to:
  - Understand natural language requests about tasks (e.g., "Show me all high-priority tasks due this week")
  - Automatically create, update, or query tasks based on user instructions via MCP tools
  - Provide intelligent task suggestions and recommendations
  - Analyze task data and generate insights
  - Handle multi-step operations (e.g., "Create a task for John with high priority and set due date to next Friday")

### **Example Use Cases**
1. User: "Create a high-priority task for reviewing the Q4 report, assign it to Sarah, and set the due date to next Monday"
   - Agent interprets request → Calls MCP tools: create_task, update_task (assignee, priority, due_date)

2. User: "What are my overdue tasks and which ones should I prioritize?"
   - Agent queries tasks → Analyzes with LLM → Returns prioritized list with reasoning

3. User: "Show me all tasks in the 'Website Redesign' project that are in-progress"
   - Agent converts to MCP query → Returns filtered results

---

## **D. Review Criteria** (Total: 100 points)

### **D1. Core Requirements** (40 points)
- [x] Database schema with correct relations, constraints, and indexes. **(8 points)**
- [x] JWT auth with role-based permissions (Admin/Manager/Member). **(8 points)**
- [x] CRUD operations for Organizations, Projects, and Tasks with business rules enforced. **(12 points)**
- [x] Status workflow (`todo → in-progress → done`), comments, file attachments, and notifications working. **(8 points)**
- [x] Basic reporting endpoints (task counts by status, overdue tasks). **(4 points)**

### **D2. MCP Server & AI Agent** (20 points)
- [ ] MCP server automatically exposes all FastAPI endpoints as tools (auto-conversion, no manual definitions). **(6 points)**
- [ ] Task AI Agent implemented and integrated with MCP server. **(4 points)**
- [ ] AI Agent successfully tests all MCP tools (create, read, update, delete operations). **(3 points)**
- [ ] LLM integration working (at least one provider: Groq, OpenAI, Anthropic, etc.). **(3 points)**
- [ ] Agent can interpret natural language and perform task operations via MCP tools. **(2 points)**
- [ ] At least 3 agent features implemented (natural language task creation, querying, updates, etc.). **(2 points)**

### **D3. Code Quality & Testing** (20 points)
- [x] Centralized error handling, logging, and consistent API response format. **(6 points)**
- [x] Configurable via `.env`, pagination for list endpoints. **(4 points)**
- [x] Test coverage ≥ 70%. **(10 points)**

### **D4. Deployment & Documentation** (20 points)
- [x] Dockerized deployment with Nginx, PostgreSQL, Redis. **(10 points)**
- [x] Health check endpoints, environment variables configured. **(4 points)**
- [x] README with setup guide, API documentation (Swagger UI). **(6 points)**

---

# 🚀 RFX Project Management System - Implementation

A powerful Project Management System Backend built to optimize team workflow, progress tracking, and detailed role-based access control. The system uses modern architecture with **FastAPI (Async)**, **PostgreSQL**, **Redis**, and is fully containerized with **Docker**.

---

## 🌟 Key Features

Based on the assignment requirements, the system provides the following feature groups:

### 1. Authentication & RBAC
* **Register / Login:** Secure JWT (JSON Web Tokens) authentication
* **Role-Based Access Control (RBAC):**
    * **ADMIN:** Full system administration, manages organizations, projects, and users
    * **MANAGER:** Manages assigned projects, adds members, assigns tasks
    * **MEMBER:** Executes tasks, updates status, adds comments

### 2. Organization & Project Management
* **Organization:** Create and manage organizational structure
* **Project:** Create new projects, set descriptions, and add members to projects

### 3. Task Management
* **CRUD Tasks:** Create, edit, delete, view task details
* **Attributes:** Status (Todo, In Progress, Done), Priority (Low, Medium, High), Deadline
* **Assignment:** Assign tasks to specific members

### 4. Collaboration
* **Comments:** Direct discussion on each Task
* **Attachments:** Upload documents and images related to Tasks
* **Notifications:** Receive notifications when assigned tasks or when there are new updates

### 5. Reports
* **Statistics:** View project progress overview, number of completed/overdue tasks, member work performance

---

## 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.11+ |
| **Framework** | FastAPI (Asynchronous) |
| **Database** | PostgreSQL 15 (Asyncpg driver) |
| **ORM** | SQLAlchemy (Async) |
| **Migrations** | Alembic |
| **Caching** | Redis |
| **Testing** | Pytest & Pytest-Cov |
| **Container** | Docker & Docker Compose |
| **Proxy** | Nginx |
| **Task Runner** | Justfile |

---

## 🚀 Setup Guide

Follow these steps to run the system on your local machine.

### 1. Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
* [Just](https://github.com/casey/just) command runner installed
* Git

### 2. Installation & Running

**Step 1: Clone repository**
```bash
git clone https://github.com/NguyenKhanhDuy2703/PROJECT_TEST_BE_RFX.git
cd PROJECT_TEST_BE_RFX
```

**Step 2: Environment Configuration**

The system is pre-configured in `docker-compose.yml` for immediate use. However, if you want to run locally (without Docker) or customize settings, you can create a `.env` file:

```bash
# Copy sample file or create new
touch .env
```

Sample `.env` content:
```ini
PROJECT_NAME="RFX Project Management"
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123456
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_DB=rfx_db

# Test Database
POSTGRES_DB_TEST=rfx_db_test

# JWT Configuration
SECRET_KEY=your_super_secret_key_change_this_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
```

**Step 3: Launch System (Using Justfile)**

Run the following command to build and start all services (Backend, DB, Redis, Nginx):

```bash
# Build and start all services
just up

# Or using docker-compose directly
docker-compose up -d --build
```

**Step 4: Run Database Migrations**

```bash
# Run migrations
just migrate

# Or using docker-compose
docker-compose exec app alembic upgrade head
```

**Step 5: Access the System**

After containers start successfully:

- **Swagger UI (API Docs):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Nginx (Reverse Proxy):** http://localhost:80
- **Health Check:** http://localhost:8000/health

---

## 📋 Available Just Commands

The project uses Justfile for convenient command management:

```bash
# Show all available commands
just --list

# Install Python dependencies
just install

# Build Docker image
just build

# Start all services (Database, Redis, App)
just up

# Stop all services
just down

# Reset database (remove all data and volumes)
just reset-db

# Create new database migration
just make-migrate "migration_name"

# Apply database migrations
just migrate

# Run FastAPI application locally (without Docker)
just run

# Run tests
just test

# Run tests with coverage report
just coverage-test
```

---

## 🧪 Testing & Coverage

The project uses an Isolated Test Environment in Docker to ensure accuracy and prevent affecting production data.

### Running Tests

```bash
# Run all tests with coverage report
just test

# Or using docker-compose directly
docker-compose run --rm app_test /bin/sh -c "alembic upgrade head && pytest -v --cov=app --cov-report=term-missing"
```

### Testing Approach
- **Isolated Test Database:** Uses separate `rfx_db_test` database
- **Automatic Rollback:** Database automatically rolls back after each test case
- **Test Containers:** PostgreSQL and Redis running in separate test containers
- **Coverage Target:** ≥ 70% code coverage

**Note:** The test database (`rfx_db_test`) automatically rolls back data after each test case to ensure a clean environment.

---

## 📂 Project Structure

```
.
├── app
│   ├── api/            # API Endpoints (Controllers)
│   │   ├── v1/         # API version 1
│   │   │   ├── auth.py
│   │   │   ├── organizations.py
│   │   │   ├── projects.py
│   │   │   ├── tasks.py
│   │   │   ├── comments.py
│   │   │   ├── notifications.py
│   │   │   └── reports.py
│   │   └── deps.py     # Dependencies (Auth, DB Session)
│   ├── core/           # System Configuration
│   │   ├── config.py   # Settings & Environment Variables
│   │   ├── security.py # JWT & Password Hashing
│   │   └── logging.py  # Centralized Logging
│   ├── db/             # Database Connection & Session
│   │   ├── base.py
│   │   └── session.py
│   ├── models/         # SQLAlchemy Models (DB Schema)
│   │   ├── user.py
│   │   ├── organization.py
│   │   ├── project.py
│   │   ├── task.py
│   │   ├── comment.py
│   │   ├── attachment.py
│   │   └── notification.py
│   ├── schemas/        # Pydantic Schemas (Request/Response Validation)
│   │   ├── user.py
│   │   ├── organization.py
│   │   ├── project.py
│   │   ├── task.py
│   │   └── ...
│   ├── services/       # Business Logic Layer
│   │   ├── auth_service.py
│   │   ├── task_service.py
│   │   ├── notification_service.py
│   │   └── ...
│   ├── utils/          # Utility Functions
│   │   ├── file_upload.py
│   │   └── validators.py
│   └── main.py         # Application Entry Point
├── migrations/         # Alembic Database Migrations
├── tests/              # Unit Tests & Integration Tests
│   ├── conftest.py     # Test Configuration & Fixtures
│   ├── test_auth.py
│   ├── test_tasks.py
│   └── ...
├── docs/               # Design Documentation
│   ├── erd.md          # Entity-Relationship Diagram
│   ├── system_design.md# System Architecture
│   └── api_docs.md     # API Reference
├── storage/            # File Upload Storage
├── nginx/              # Nginx Configuration
│   └── nginx.conf
├── docker-compose.yml  # Docker Services Configuration
├── Dockerfile          # Backend Image Definition
├── Justfile            # Command Runner Configuration
├── requirements.txt    # Python Dependencies
├── .env.example        # Environment Variables Template
└── README.md           # Project Documentation
```

---

## 📚 Design Documentation

Detailed system design and database documentation:
- **Database Schema:** [ER Diagram](docs/erd.md) or https://www.drawdb.app/editor?shareId=d4a8c1ec5012f1943bda6b298156528c
- **API Reference:** [API Documentation](docs/api_docs.md) or visit http://localhost:8000/api/v1/
- **System Architecture:** [System Design](docs/system_design.md)

## 🔒 Security Features

- **JWT Authentication:** Secure token-based authentication
- **Password Hashing:** Bcrypt algorithm for password encryption
- **RBAC:** Role-based access control (Admin/Manager/Member)
- **CORS:** Configurable Cross-Origin Resource Sharing
- **Rate Limiting:** Redis-based request rate limiting
- **Input Validation:** Pydantic schemas for request validation

---

## 📊 API Endpoints Overview

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token

### Organizations
- `GET /api/v1/organizations` - List organizations
- `POST /api/v1/organizations` - Create organization (Admin only)
- `GET /api/v1/organizations/{id}` - Get organization details

### Projects
- `GET /api/v1/projects` - List projects
- `POST /api/v1/projects` - Create project
- `PUT /api/v1/projects/{id}` - Update project
- `POST /api/v1/projects/{id}/members` - Add project member

### Tasks
- `GET /api/v1/tasks` - List tasks (with filters(status , priority ... ) & pagination)
- `POST /api/v1/tasks` - Create task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task
- `POST /api/v1/tasks/{id}/comments` - Add comment
- `POST /api/v1/tasks/{id}/attachments` - Upload attachment

### Notifications
- `GET /api/v1/notifications` - Get user notifications
- `PUT /api/v1/notifications/{id}/read` - Mark as read

### Reports
- `GET /api/v1/reports/project/{id}/tasks` - Task count by status
- `GET /api/v1/reports/project/{id}/overdue` - Overdue tasks

For complete API documentation, visit: http://localhost:8000/docs

---

## 🚀 Deployment

The system is fully Dockerized and ready for deployment:

```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# With health checks
docker-compose ps
```

### Health Check Endpoints
- `GET /health` - System health status
- `GET /health/db` - Database connection status
- `GET /health/redis` - Redis connection status

---

## 🤝 Contributing

This is an assignment project. For evaluation purposes only.

---

## 👨‍💻 Developer

**Nguyen Khanh Duy**
- GitHub: [@NguyenKhanhDuy2703](https://github.com/NguyenKhanhDuy2703)
- Email: nguyenkhanhduy2703@gmail.com

---

## 📄 License

Copyright (c) River Flow Solutions, Jsc. 2026. All rights reserved.
Used for candidate evaluation purposes only.