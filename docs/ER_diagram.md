# ER Diagram – Task Management System

## Entities

### User
- id (PK)
- email
- password_hash
- full_name
- role (admin | manager | member)
- organization_id (FK)
- created_at

### Organization
- id (PK)
- name
- created_at

### Project
- id (PK)
- name
- organization_id (FK)
- created_at

### Task
- id (PK)
- project_id (FK)
- title
- description
- status (todo | in_progress | done)
- priority (low | medium | high)
- assignee_id (FK → User)
- due_date
- created_at

### Comment
- id (PK)
- task_id (FK)
- user_id (FK)
- content
- created_at

### Notification
- id (PK)
- user_id (FK)
- task_id (FK)
- type
- is_read
- created_at

## Relationships

- Organization 1 — * User
- Organization 1 — * Project
- Project 1 — * Task
- Task 1 — * Comment
- User 1 — * Comment
- User 1 — * Notification
- Task 1 — * Notification

## ER Overview

