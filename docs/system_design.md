# System Design Documentation - RFX Project Management System

## 1. Overview

**RFX Project Management System** is a Backend project management solution built on asynchronous technology platform, focusing on high performance and scalability. The system provides features for managing organizations, projects, tasks, and progress reporting.

---

## 2. High-Level Architecture

The system is fully containerized in **Docker**, using a Microservices-ready model with **Nginx** as a Reverse Proxy routing requests to Backend, Database, and Cache.

```mermaid
graph TD
    User[User Client / Frontend] -->|HTTP/HTTPS| Nginx[Nginx Reverse Proxy]
    
    subgraph Docker Network
        Nginx -->|Proxy Pass| API[FastAPI Backend Server]
        API -->|Read/Write Data| DB[(PostgreSQL Primary)]
        API -->|Cache/Session| Cache[(Redis)]
        API -->|Logs| Logger[Logging System]
    end

    subgraph Storage & Volumes
        DB --> PgData[Volume: postgres_data]
        API --> FileStore[File Storage: /app/storage]
    end
```

---

## 3. Tech Stack & Components

| Component | Technology | Description |
|-----------|-----------|-------------|
| Language | Python 3.11+ | Utilizing modern Type Hinting and Async I/O |
| Web Framework | FastAPI | High-performance framework with automatic OpenAPI support |
| Database | PostgreSQL 15 | Robust relational database using asyncpg driver |
| ORM | SQLAlchemy (Async) | Object Relational Mapper |
| Migrations | Alembic | Database schema migration management |
| Caching | Redis | Cache storage, session management, and Rate Limiting support |
| Testing | Pytest | Automated testing framework (Unit & Integration Test) |
| Container | Docker & Compose | Consistent deployment environment packaging |
| Web Server | Nginx | Reverse Proxy and Static Files serving |

---

## 4. Layered Architecture

Source code is organized following the **Controller - Service - Repository** pattern to ensure "Separation of Concerns" principle.

```mermaid
classDiagram
    class ClientRequest {
        +HTTP Methods (GET, POST...)
    }
    class Router_Controller {
        +Validate Request (Pydantic)
        +Dependency Injection
        +Call Service
    }
    class Service_Layer {
        +Business Logic
        +RBAC Checks
        +Call DB/Redis
    }
    class Data_Access_Models {
        +SQLAlchemy Models
        +DB Transactions
    }
    class Infrastructure {
        +PostgreSQL
        +Redis
    }

    ClientRequest --> Router_Controller : Request
    Router_Controller --> Service_Layer : DTOs
    Service_Layer --> Data_Access_Models : Entities
    Data_Access_Models --> Infrastructure : SQL / Commands
```

### 4.1. Main Modules

- **API Layer** (`app/api`): Receives requests, validates input data (Pydantic Schemas), and returns standardized responses
- **Service Layer** (`app/services`): Contains core business logic (e.g., report calculations, file upload processing, task creation logic)
- **Model Layer** (`app/models`): Defines database table structure using SQLAlchemy
- **Core** (`app/core`): System configuration, Security, Logging, and Redis connection

---

## 5. Main Processing Flows (Sequence Diagrams)

### 5.1. Login Flow

Describes how users log in and receive JWT Access Token.

```mermaid
sequenceDiagram
    participant U as User
    participant API as FastAPI
    participant DB as PostgreSQL
    
    U->>API: POST /auth/login (email, password)
    API->>DB: Query User by Email
    DB-->>API: User Data (Hashed Password)
    API->>API: Verify Password (Bcrypt)
    
    alt Password Valid
        API->>API: Generate JWT Token
        API-->>U: Return 200 OK + Access Token
    else Password Invalid
        API-->>U: Return 401 Unauthorized
    end
```

### 5.2. Create Task Flow

Describes the interaction between layers when a user creates a new task.

```mermaid
sequenceDiagram
    participant Client
    participant Controller
    participant Service
    participant DB
    
    Client->>Controller: POST /tasks/ (Token, TaskData)
    Controller->>Controller: Validate Token (Auth Middleware)
    Controller->>Service: create_task(user_id, TaskData)
    
    Service->>Service: Check User Permissions (RBAC)
    Service->>Service: Validate Project Existence
    
    Service->>DB: INSERT INTO tasks
    DB-->>Service: Task Object (New ID)
    
    Service-->>Controller: Task DTO
    Controller-->>Client: 201 Created + Task JSON
```

---

## 6. Security Design

### 6.1. Authentication

- **Standard**: OAuth2 with Password Flow
- **Token**: JSON Web Tokens (JWT) containing `sub` (user_id) and `role`
- **Encryption**: Passwords are hashed using bcrypt algorithm before storing in DB

### 6.2. Authorization (RBAC)

The system implements Role-Based Access Control:

- **ADMIN**: Full system administration rights, manages Organizations and Projects
- **MANAGER**: Manages projects, adds members, and assigns tasks within their organization
- **MEMBER**: Can only view assigned projects and update status of assigned tasks

---

