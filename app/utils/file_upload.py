import os
import shutil
from datetime import datetime, timezone
from fastapi import UploadFile, HTTPException
from typing import Tuple

# configurations
UPLOAD_DIRECTORY = "storage/uploads" 
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
MAX_FILE_SIZE = 5 * 1024 * 1024 

async def handle_file_upload(file: UploadFile) -> Tuple[str, int, str]:
    
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0) 

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400, 
            detail=f"File size exceeds the maximum limit of {MAX_FILE_SIZE // (1024 * 1024)}MB"
        )
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    sanitized_filename = file.filename.replace(" ", "_")
    unique_filename = f"{timestamp}_{sanitized_filename}"
    file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")
    finally:
        await file.close()

    url_file = f"/static/{unique_filename}" 

    return url_file, file_size, file.filename