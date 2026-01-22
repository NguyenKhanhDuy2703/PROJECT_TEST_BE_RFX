# app/api/v1/report.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.report_service import ReportService
from app.schemas.report_schema import ProjectReportResponse
from app.core.auth import allow_all 

router = APIRouter(
    prefix="/api/v1/reports",
    tags=["reports"],
)

def get_report_service(db: AsyncSession = Depends(get_db)) -> ReportService:
    return ReportService(db)

@router.get("/project/{project_id}", response_model=ProjectReportResponse, status_code=status.HTTP_200_OK)
async def get_project_report(
    project_id: int,
    current_user = Depends(allow_all),
    report_service: ReportService = Depends(get_report_service),
):
    try:
        report_data = await report_service.generate_task_report(project_id, current_user)
        return report_data
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}",
        )