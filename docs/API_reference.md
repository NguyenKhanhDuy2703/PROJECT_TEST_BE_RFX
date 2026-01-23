# API Reference Documentation

This document provides detailed information about the **RFX Project Management System** API endpoints.

- **Base URL:** `http://localhost:8000/api/v1`
- **Authentication:** Bearer Token (JWT)
- **Interactive Docs:** [Swagger UI](http://localhost:8000/docs) | [ReDoc](http://localhost:8000/redoc)

---

## 📋 Table of Contents

1. [Authentication](#1-authentication)
2. [Organizations](#2-organizations)
3. [Projects](#3-projects)
4. [Tasks](#4-tasks)
5. [Comments](#5-comments)
6. [Attachments](#6-attachments)
7. [Notifications](#7-notifications)
8. [Reports](#8-reports)
9. [HTTP Status Codes](#9-http-status-codes)

---

## 1. Authentication

### 1.1. Register New Account

Create a new user account.

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "StrongPassword123!",
  "full_name": "John Doe",
  "org_id": 1,
  "role": "MEMBER"
}
```

**Available Roles:**
- `ADMIN` - Full system administration
- `MANAGER` - Project management
- `MEMBER` - Task execution

**Response (201 Created):**
```json
{
  "user_id": 10,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "MEMBER",
  "org_id": 1
}
```

---

### 1.2. Login

Authenticate and receive an access token.

**Endpoint:** `POST /auth/login`

**Content-Type:** `application/x-www-form-urlencoded`

**Form Data:**
- `username` - User email address
- `password` - User password

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1Ni...",
  "token_type": "bearer",
  "role": "MEMBER",
  "user_id": 10
}
```

**Usage:**
Include the token in subsequent requests:
```
Authorization: Bearer eyJhbGciOiJIUzI1Ni...
```

---

## 2. Organizations

### 2.1. Create Organization

Create a new organization.

**Endpoint:** `POST /orgs/`

**Permissions:** `ADMIN`

**Request Body:**
```json
{
  "name": "RFX Corporation"
}
```

**Response (201 Created):**
```json
{
  "org_id": 1,
  "name": "RFX Corporation",
  "created_at": "2026-01-20T10:00:00Z"
}
```

---

### 2.2. List Organizations

Get all organizations the user has access to.

**Endpoint:** `GET /orgs/`

**Permissions:** Authenticated User

**Response (200 OK):**
```json
[
  {
    "org_id": 1,
    "name": "RFX Corporation",
    "created_at": "2026-01-20T10:00:00Z"
  },
  {
    "org_id": 2,
    "name": "Tech Startup Inc.",
    "created_at": "2026-01-22T14:30:00Z"
  }
]
```

---

## 3. Projects

### 3.1. Create Project

Create a new project within an organization.

**Endpoint:** `POST /projects/`

**Permissions:** `ADMIN`, `MANAGER`

**Request Body:**
```json
{
  "name": "E-commerce Website",
  "description": "Building a new online store platform",
  "org_id": 1
}
```

**Response (201 Created):**
```json
{
  "project_id": 5,
  "name": "E-commerce Website",
  "description": "Building a new online store platform",
  "org_id": 1,
  "created_by": 1,
  "created_at": "2026-01-23T09:15:00Z"
}
```

---

### 3.2. List Projects

Get all projects the user is a member of.

**Endpoint:** `GET /projects/`

**Query Parameters:**
- `skip` - Number of records to skip (default: 0)
- `limit` - Maximum number of records to return (default: 100)

**Response (200 OK):**
```json
[
  {
    "project_id": 5,
    "name": "E-commerce Website",
    "description": "Building a new online store platform",
    "org_id": 1,
    "member_count": 8,
    "task_count": 23
  }
]
```

---

### 3.3. Add Project Member

Add a user to a project.

**Endpoint:** `POST /projects/{project_id}/members`

**Permissions:** `ADMIN`, `MANAGER` (of the project)

**Request Body:**
```json
{
  "user_id": 5
}
```

**Response (201 Created):**
```json
{
  "message": "User added to project successfully",
  "project_id": 5,
  "user_id": 5
}
```

---

### 3.4. Remove Project Member

Remove a user from a project.

**Endpoint:** `DELETE /projects/{project_id}/members/{user_id}`

**Permissions:** `ADMIN`, `MANAGER` (of the project)

**Response (200 OK):**
```json
{
  "message": "User removed from project successfully"
}
```

---

## 4. Tasks

### 4.1. Create Task

Create a new task in a project.

**Endpoint:** `POST /tasks/`

**Permissions:** Project `MEMBER`

**Request Body:**
```json
{
  "project_id": 5,
  "title": "Design Database Schema",
  "description": "Create ERD diagram and SQL migration script",
  "status": "TO_DO",
  "priority": "HIGH",
  "due_date": "2026-02-01T17:00:00Z",
  "assignee_id": 5
}
```

**Field Enums:**

**Status:**
- `TO_DO` - Not started
- `IN_PROGRESS` - Currently being worked on
- `COMPLETED` - Finished

**Priority:**
- `LOW` - Low priority
- `MEDIUM` - Medium priority
- `HIGH` - High priority

**Response (201 Created):**
```json
{
  "task_id": 101,
  "project_id": 5,
  "title": "Design Database Schema",
  "description": "Create ERD diagram and SQL migration script",
  "status": "TO_DO",
  "priority": "HIGH",
  "due_date": "2026-02-01T17:00:00Z",
  "assignee_id": 5,
  "created_by": 1,
  "created_at": "2026-01-23T10:30:00Z"
}
```

---

### 4.2. List Tasks

Get all tasks with optional filtering.

**Endpoint:** `GET /tasks/`

**Query Parameters:**
- `project_id` - Filter by project (optional)
- `status` - Filter by status (optional)
- `assignee_id` - Filter by assignee (optional)
- `priority` - Filter by priority (optional)
- `skip` - Pagination offset (default: 0)
- `limit` - Results per page (default: 100)

**Example Request:**
```
GET /tasks/?project_id=5&status=IN_PROGRESS&limit=20
```

**Response (200 OK):**
```json
[
  {
    "task_id": 101,
    "title": "Design Database Schema",
    "status": "IN_PROGRESS",
    "priority": "HIGH",
    "due_date": "2026-02-01T17:00:00Z",
    "assignee_id": 5,
    "assignee_name": "John Doe",
    "created_by": 1,
    "project_name": "E-commerce Website"
  }
]
```

---

### 4.3. Get Task Details

Get detailed information about a specific task.

**Endpoint:** `GET /tasks/{task_id}`

**Response (200 OK):**
```json
{
  "task_id": 101,
  "project_id": 5,
  "title": "Design Database Schema",
  "description": "Create ERD diagram and SQL migration script",
  "status": "IN_PROGRESS",
  "priority": "HIGH",
  "due_date": "2026-02-01T17:00:00Z",
  "assignee_id": 5,
  "created_by": 1,
  "created_at": "2026-01-23T10:30:00Z",
  "updated_at": "2026-01-23T14:20:00Z",
  "comments_count": 3,
  "attachments_count": 2
}
```

---

### 4.4. Update Task

Update task information or status.

**Endpoint:** `PUT /tasks/{task_id}`

**Permissions:** Task assignee or Project Manager/Admin

**Request Body (Partial Update):**
```json
{
  "status": "COMPLETED",
  "description": "ERD completed and reviewed by team"
}
```

**Response (200 OK):**
```json
{
  "task_id": 101,
  "title": "Design Database Schema",
  "status": "COMPLETED",
  "updated_at": "2026-01-23T16:45:00Z"
}
```

---

### 4.5. Delete Task

Delete a task from the system.

**Endpoint:** `DELETE /tasks/{task_id}`

**Permissions:** `ADMIN`, `MANAGER` (of the project)

**Response (200 OK):**
```json
{
  "message": "Task deleted successfully"
}
```

---

## 5. Comments

### 5.1. Add Comment

Add a comment to a task.

**Endpoint:** `POST /comments/`

**Request Body:**
```json
{
  "task_id": 101,
  "content": "Updated the design with the new requirements. Please review."
}
```

**Response (201 Created):**
```json
{
  "comment_id": 45,
  "task_id": 101,
  "user_id": 5,
  "content": "Updated the design with the new requirements. Please review.",
  "created_at": "2026-01-23T11:20:00Z"
}
```

---

### 5.2. Get Task Comments

Get all comments for a specific task.

**Endpoint:** `GET /comments/task/{task_id}`

**Response (200 OK):**
```json
[
  {
    "comment_id": 45,
    "task_id": 101,
    "user_id": 5,
    "user_name": "John Doe",
    "content": "Updated the design with the new requirements. Please review.",
    "created_at": "2026-01-23T11:20:00Z"
  },
  {
    "comment_id": 46,
    "task_id": 101,
    "user_id": 3,
    "user_name": "Jane Smith",
    "content": "Looks good! Approved.",
    "created_at": "2026-01-23T12:00:00Z"
  }
]
```

---

### 5.3. Update Comment

Update an existing comment.

**Endpoint:** `PUT /comments/{comment_id}`

**Permissions:** Comment author only

**Request Body:**
```json
{
  "content": "Updated content with additional information."
}
```

**Response (200 OK):**
```json
{
  "comment_id": 45,
  "content": "Updated content with additional information.",
  "updated_at": "2026-01-23T13:00:00Z"
}
```

---

### 5.4. Delete Comment

Delete a comment.

**Endpoint:** `DELETE /comments/{comment_id}`

**Permissions:** Comment author or `ADMIN`/`MANAGER`

**Response (200 OK):**
```json
{
  "message": "Comment deleted successfully"
}
```

---

## 6. Attachments

### 6.1. Upload File

Upload a file attachment to a task.

**Endpoint:** `POST /attachments/`

**Content-Type:** `multipart/form-data`

**Form Data:**
- `task_id` - ID of the task (integer)
- `file` - File binary data (max 5MB)

**Limitations:**
- Maximum file size: 5MB per file
- Maximum attachments per task: 3 files

**Response (201 Created):**
```json
{
  "attachment_id": 55,
  "task_id": 101,
  "file_name": "design_v2.png",
  "file_url": "/storage/uploads/20260123_design_v2.png",
  "file_size": 245678,
  "uploaded_by": 5,
  "created_at": "2026-01-23T14:30:00Z"
}
```

---

### 6.2. Get Task Attachments

Get all attachments for a specific task.

**Endpoint:** `GET /attachments/task/{task_id}`

**Response (200 OK):**
```json
[
  {
    "attachment_id": 55,
    "file_name": "design_v2.png",
    "file_url": "/storage/uploads/20260123_design_v2.png",
    "file_size": 245678,
    "uploaded_by": 5,
    "uploader_name": "John Doe",
    "created_at": "2026-01-23T14:30:00Z"
  }
]
```

---

### 6.3. Delete Attachment

Delete a file attachment.

**Endpoint:** `DELETE /attachments/{attachment_id}`

**Permissions:** Uploader or `ADMIN`/`MANAGER`

**Response (200 OK):**
```json
{
  "message": "Attachment deleted successfully"
}
```

---

## 7. Notifications

### 7.1. Get User Notifications

Get all notifications for the current user.

**Endpoint:** `GET /notifications/`

**Query Parameters:**
- `is_read` - Filter by read status (optional, boolean)
- `skip` - Pagination offset (default: 0)
- `limit` - Results per page (default: 50)

**Response (200 OK):**
```json
[
  {
    "notification_id": 123,
    "user_id": 5,
    "title": "New Task Assigned",
    "message": "You have been assigned to task: Design Database Schema",
    "type": "TASK_ASSIGNED",
    "is_read": false,
    "created_at": "2026-01-23T10:30:00Z",
    "related_task_id": 101
  },
  {
    "notification_id": 124,
    "user_id": 5,
    "title": "Task Status Changed",
    "message": "Task 'API Integration' status changed to COMPLETED",
    "type": "TASK_STATUS_CHANGED",
    "is_read": true,
    "created_at": "2026-01-23T09:15:00Z",
    "related_task_id": 98
  }
]
```

**Notification Types:**
- `TASK_ASSIGNED` - User assigned to a task
- `TASK_STATUS_CHANGED` - Task status updated
- `COMMENT_ADDED` - New comment on user's task
- `PROJECT_ADDED` - User added to a project

---

### 7.2. Mark Notification as Read

Mark a specific notification as read.

**Endpoint:** `PUT /notifications/{notification_id}/read`

**Response (200 OK):**
```json
{
  "notification_id": 123,
  "is_read": true,
  "read_at": "2026-01-23T15:00:00Z"
}
```

---

### 7.3. Mark All Notifications as Read

Mark all user notifications as read.

**Endpoint:** `PUT /notifications/mark-all-read`

**Response (200 OK):**
```json
{
  "message": "All notifications marked as read",
  "updated_count": 5
}
```

---

## 8. Reports

### 8.1. Project Progress Report

Get detailed progress statistics for a project.

**Endpoint:** `GET /reports/projects/{project_id}`

**Permissions:** `ADMIN`, `MANAGER` (of the project)

**Response (200 OK):**
```json
{
  "project_id": 5,
  "project_name": "E-commerce Website",
  "total_tasks": 20,
  "completed_tasks": 15,
  "in_progress_tasks": 3,
  "todo_tasks": 2,
  "overdue_tasks": 1,
  "completion_rate": 75.0,
  "tasks_by_priority": {
    "HIGH": 8,
    "MEDIUM": 7,
    "LOW": 5
  },
  "report_generated_at": "2026-01-23T16:00:00Z"
}
```

---

### 8.2. Overdue Tasks Report

Get all overdue tasks in a project.

**Endpoint:** `GET /reports/projects/{project_id}/overdue`

**Permissions:** `ADMIN`, `MANAGER`, project `MEMBER`

**Response (200 OK):**
```json
[
  {
    "task_id": 89,
    "title": "Update Documentation",
    "status": "IN_PROGRESS",
    "priority": "MEDIUM",
    "due_date": "2026-01-20T17:00:00Z",
    "assignee_id": 7,
    "assignee_name": "Mike Johnson",
    "days_overdue": 3
  }
]
```

---

### 8.3. User Performance Report

Get task completion statistics for a user.

**Endpoint:** `GET /reports/users/{user_id}/performance`

**Permissions:** `ADMIN`, `MANAGER`, or self

**Query Parameters:**
- `start_date` - Report start date (optional)
- `end_date` - Report end date (optional)

**Response (200 OK):**
```json
{
  "user_id": 5,
  "user_name": "John Doe",
  "period": {
    "start_date": "2026-01-01",
    "end_date": "2026-01-31"
  },
  "total_tasks_assigned": 15,
  "completed_tasks": 12,
  "in_progress_tasks": 2,
  "overdue_tasks": 1,
  "completion_rate": 80.0,
  "average_completion_time_hours": 24.5
}
```

---

## 9. HTTP Status Codes

The system uses standard HTTP status codes:

| Code | Meaning | Description |
|------|---------|-------------|
| `200` | OK | Request successful |
| `201` | Created | Resource created successfully |
| `204` | No Content | Request successful with no response body |
| `400` | Bad Request | Invalid request data |
| `401` | Unauthorized | Not authenticated or token expired |
| `403` | Forbidden | Insufficient permissions |
| `404` | Not Found | Resource not found |
| `422` | Validation Error | Data validation failed (missing required fields) |
| `500` | Server Error | Internal server error |

---

## 🔗 Additional Resources

- **Live API Documentation:** http://localhost:8000/docs
- **Alternative Documentation:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **GitHub Repository:** https://github.com/NguyenKhanhDuy2703/PROJECT_TEST_BE_RFX

---

**Last Updated:** January 23, 2026  
**API Version:** v1  
**Developed by:** Nguyen Khanh Duy