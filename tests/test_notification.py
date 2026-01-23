from app.models.notification import Notification # Import model này
from sqlalchemy import select
import pytest
from app.models.task import StatusEnum
import pytest
from sqlalchemy import select
from app.models.notification import Notification, NotificationTypeEnum # Nhớ import Enum
from app.models.project_member import Project_member
from app.models.task import StatusEnum
from datetime import datetime, timezone

# --- CASE 01: Notify user when assigned to task ---
@pytest.mark.asyncio
async def test_notify_user_when_assigned(
    client, 
    manager_auth_headers, 
    test_project, 
    test_user_member, 
    db_session, 
    test_user_manager
):
    # 1. SETUP: Add Manager vào Project (Để có quyền tạo task)
    pm = Project_member(
        project_id=test_project.project_id,
        user_id=test_user_manager.user_id, 
        joined_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )
    db_session.add(pm)
    await db_session.commit()

    # 2. ACTION: Manager tạo task gán cho Member
    task_payload = {
        "title": "Task for Notification Test",
        "description": "Checking notification trigger",
        "project_id": test_project.project_id,
        "priority": "HIGH",
        "status": "TO_DO",
        "assignee_id": test_user_member.user_id, 
        "due_date": "2026-12-31T00:00:00"
    }

    response = await client.post("/api/v1/tasks/create", json=task_payload, headers=manager_auth_headers)
    assert response.status_code == 201
    query_notif = select(Notification).where(
        Notification.user_id == test_user_member.user_id,
        Notification.is_read == False
    ).order_by(Notification.created_at.desc())
    
    result = await db_session.execute(query_notif)
    notification = result.scalars().first()

    assert notification is not None, "Notification record was not created in DB"
    assert "assigned" in notification.content.lower()
    assert notification.type == NotificationTypeEnum.TASK_ASSIGNED
