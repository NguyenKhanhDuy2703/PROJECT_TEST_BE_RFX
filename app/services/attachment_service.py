from  fastapi import HTTPException, status , UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.attachment import Attachment
from app.utils.file_upload import handle_file_upload
from datetime import datetime , timezone
from sqlalchemy import select
from app.models.task import Task
from app.models.user import User
class AttachmentService:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def upload_attachment( self, task_id: int, file_path: UploadFile , current_user ) -> Attachment:

        check_user_in_org = await self.db.execute ( select ( User).where ( User.user_id == current_user.user_id  , User.org_id == current_user.org_id ) )
        user = check_user_in_org.scalars().first()
        if not user :
            raise HTTPException ( status_code =403 , detail = "Access denied : You are not in the organization " )
        
        check_user = await self.db.execute ( select ( Task).where ( Task.task_id == task_id  ) )
        check_user_task = check_user.scalars().first()
        if not check_user_task or check_user_task.assignee_id != current_user.user_id :
            raise HTTPException ( status_code =403 , detail = "Access denied : You are not assigned to this task " )    
        
        check_task = await self.db.execute ( select ( Task).where ( Task.task_id == task_id  ) )
        task = check_task.scalars().first()
        if not task :
            raise HTTPException ( status_code =404 , detail = "Task does not exist " )
        
        check_number_attachments = await self.db.execute ( select ( Attachment).where ( Attachment.task_id == task_id  ) )
        attachments = check_number_attachments.scalars().all()
        if len ( attachments ) >= 3 :
            raise HTTPException ( status_code =400 , detail = "Maximum number of attachments (3) reached for this task " )
        file_url, file_size, file_name = await handle_file_upload(file_path)
        new_attachment = Attachment (
            task_id = task_id ,
            user_id = current_user.user_id ,
            file_name = file_name,
            file_url = file_url ,
            file_size = file_size ,
            uploaded_at = datetime.now ( timezone.utc ).replace ( tzinfo = None )
        )
        self.db.add ( new_attachment )
        await self.db.commit()
        await self.db.refresh ( new_attachment )
        return new_attachment
